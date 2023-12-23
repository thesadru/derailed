import datetime
from typing import Annotated

import pydantic
from fastapi import APIRouter, Request

from api.src.derailed_api import meta

from ..factors.channel_factors import get_channel
from ..factors.user_factors import get_user_from_token

router = APIRouter()
db = meta.db


class CreateMessage(pydantic.BaseModel):
    content: Annotated[str, pydantic.Field(min_length=1, max_length=2048)]


@router.post("/channels/{channel_id}/messages")
async def create_message(request: Request, channel_id: int, model: CreateMessage):
    async with db.acquire() as session:
        user = await get_user_from_token(request, session)
        channel = await get_channel(channel_id, user["id"], session)
        channel_members = await session.fetch(
            "SELECT user_id FROM channel_members WHERE channel_id = $1;", channel["id"]
        )

        message = await session.fetchrow(
            "INSERT INTO messages (id, channel_id, author_id, content, timestamp) VALUES ($1, $2, $3, $4, $5) RETURNING *;",
            meta.create_snowflake(),
            channel["id"],
            user["id"],
            model.content,
            datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
        )

        assert message is not None

        msg = dict(message)

        user_ids = []

        for member in channel_members:
            user_ids.append(member["user_id"])

        await meta.publish_channel("MESSAGE_CREATE", user_ids, msg)

        return msg


@router.get("/channels/{channel_id}/messages")
async def get_channel_messages(
    request: Request, channel_id: int, after: int = 0, before: int = 0
):
    async with db.acquire() as session:
        user = await get_user_from_token(request, session)
        await get_channel(channel_id, user["id"], session)

        if before != 0:
            messages = await session.fetchrow(
                f"SELECT * FROM messages WHERE channel_id = $1 AND id > $2 AND id < $3 ORDER BY id DESC LIMIT 32;",
                channel_id,
                after,
                before,
            )
        else:
            messages = await session.fetchrow(
                f"SELECT * FROM messages WHERE channel_id = $1 AND id > $2 ORDER BY id DESC LIMIT 32;",
                channel_id,
                after,
            )

        return messages
