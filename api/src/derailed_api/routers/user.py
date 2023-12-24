from typing import Annotated, Any, Literal, TypedDict
from uuid import uuid4

import argon2
import asyncpg.exceptions
import itsdangerous
import pydantic
from fastapi import APIRouter, Request

from ..error import Error
from ..factors.user_factors import get_user_from_token
from ..meta import meta
from ..missing import MISSING, Maybe

router = APIRouter()
pwhasher = argon2.PasswordHasher()


class Register(pydantic.BaseModel):
    email: pydantic.EmailStr
    username: Annotated[
        str,
        pydantic.Field(
            min_length=3, max_length=32, pattern=r"^[a-z0-9]+(?:[._][a-z0-9]+)*$"
        ),
    ]
    password: Annotated[str, pydantic.Field(min_length=8, max_length=128)]
    invite_code: Annotated[str, pydantic.Field(max_length=100, min_length=1)]


@router.post("/register", status_code=201)
async def register(model: Register):
    async with meta.db.acquire() as session:
        owner_id = await session.fetchval(
            "SELECT owner_id FROM invite_codes WHERE id = $1;", model.invite_code
        )

        if owner_id is None:
            raise Error(1007, "Invite code does not exist or is expired or used")

        async with session.transaction():
            try:
                user_rec = await session.fetchrow(
                    "INSERT INTO users (id, email, username, password, invited_by) VALUES ($1, $2, $3, $4, $5) RETURNING *;",
                    meta.create_snowflake(),
                    model.email.lower(),
                    model.username.lower(),
                    pwhasher.hash(model.password),
                    owner_id,
                )
            except asyncpg.exceptions.UniqueViolationError:
                raise Error(1000, "username or email must be unique")

            assert user_rec is not None

            await session.fetch(
                "INSERT INTO user_settings (user_id) VALUES ($1);", user_rec["id"]
            )
            await session.fetch(
                "DELETE FROM invite_codes WHERE id = $1;", model.invite_code
            )

            user = dict(user_rec)
            user["invite_codes"] = []

            for _ in range(5):
                invite_code = str(uuid4())
                await session.fetch(
                    "INSERT INTO invite_codes (id, owner_id) VALUES ($1, $2);",
                    invite_code,
                    user["id"],
                )
                user["invite_codes"].append(invite_code)

            signer = itsdangerous.TimestampSigner(user.pop("password"))

            user["_token"] = signer.sign(user["id"])

        return user


class Login(pydantic.BaseModel):
    email: Annotated[str, pydantic.Field(min_length=5, max_length=128)]
    password: Annotated[str, pydantic.Field(min_length=8, max_length=128)]


@router.post("/login")
async def login(model: Login):
    async with meta.db.acquire() as session:
        user = await session.fetchrow(
            "SELECT * FROM users WHERE email = $1;", model.email.lower()
        )

        if user is None:
            raise Error(1005, "Invalid email")

        user = dict(user)

        pw = user.pop("password")

        try:
            pwhasher.verify(pw, model.password)
        except argon2.exceptions.VerifyMismatchError:
            raise Error(1006, "Invalid password")

        signer = itsdangerous.TimestampSigner(pw)

        user["_token"] = signer.sign(user["id"])

        return user


class PatchUser(pydantic.BaseModel):
    email: Annotated[Maybe[str], pydantic.Field(MISSING, min_length=5, max_length=128)]
    username: Annotated[
        Maybe[str], pydantic.Field(MISSING, min_length=3, max_length=32)
    ]
    password: Annotated[
        Maybe[str], pydantic.Field(MISSING, min_length=8, max_length=128)
    ]


@router.patch("/users/@me")
async def modify_user(request: Request, model: PatchUser):
    async with meta.db.acquire() as session:
        user = await get_user_from_token(request, session)

        async with session.transaction():
            if model.email:
                if model.email != user["email"]:
                    user["email"] = model.email.lower()
                    try:
                        await session.execute(
                            "UPDATE users SET email = $1 WHERE id = $2;",
                            model.email.lower(),
                            user["id"],
                        )
                    except asyncpg.UniqueViolationError:
                        raise Error(1000, "email must be unique")
            if model.username:
                if model.username != user["username"]:
                    user["username"] = model.username.lower()
                    try:
                        await session.execute(
                            "UPDATE users SET username = $1 WHERE id = $2",
                            model.username.lower(),
                            user["id"],
                        )
                    except asyncpg.UniqueViolationError:
                        raise Error(1000, "username must be unique")
            if model.password:
                await session.execute(
                    "UPDATE users SET password = $1 WHERE id = $2",
                    pwhasher.hash(model.password),
                    user["id"],
                )

        await meta.publish_user("USER_UPDATE", user["id"], user)

        return user


## NOTE: user relationships


class Relationship(TypedDict):
    origin_user_id: int
    target_user_id: int
    # NOTE: VALUES:
    # 0: friend
    # 1: blocked
    # 2: incoming
    # 3: outgoing
    relation: int


class RelationshipType(pydantic.BaseModel):
    type: Literal[0, 1, 2, None]


@router.put("/users/by-username/{username}/relationship")
async def put_relationship(request: Request, username: str, model: RelationshipType):
    async with meta.db.acquire() as session:
        async with session.transaction():
            user = await get_user_from_token(request, session)
            target = await session.fetchrow(
                "SELECT * FROM users WHERE username = $1;", username.lower()
            )
            assert target is not None

            target_user_relation: int = await session.fetchval(
                "SELECT relation FROM relationships WHERE origin_user_id = $1 AND target_user_id = $2;",
                target["id"],
                user["id"],
            )

            if target_user_relation == 0 and model.type != None:
                raise Error(1002, "User has blocked you")

            if model.type == 1 and target_user_relation != 3:
                raise Error(1008, "Cannot accept friend request which does not exist")

            await session.fetch(
                "DELETE FROM relationships WHERE origin_user_id = $1 AND target_user_id = $2;",
                user["id"],
                target["id"],
            )
            await session.fetch(
                "DELETE FROM relationships WHERE origin_user_id = $1 AND target_user_id = $2;",
                target["id"],
                user["id"],
            )

            if model.type == None:
                return ""

            relationship = await session.fetchrow(
                "INSERT INTO relationships (origin_user_id, target_user_id, relation) VALUES ($1, $2, $3)",
                user["id"],
                target["id"],
                model.type,
            )

            new_foreign_type = 1

            if model.type == 2:
                new_foreign_type = 3

            if model.type == 2 or model.type == 1:
                await session.fetch(
                    "INSERT INTO relationships (origin_user_id, target_user_id, relation) VALUES ($1, $2, $3);",
                    target["id"],
                    user["id"],
                    new_foreign_type,
                )

            assert relationship is not None

            # very janky query, but it works.
            if relationship["relation"] == 1:
                dm_channel = await session.fetchrow(
                    "SELECT * FROM channels WHERE id IN (SELECT channel_id FROM channel_members WHERE user_id = $1 INTERSECT SELECT channel_id FROM channel_members WHERE user_id = $2) AND type = 0;",
                    user["id"],
                    target["id"],
                )

                if dm_channel is None:
                    channel: dict[str, Any] = dict(
                        await session.fetchrow(  # type: ignore
                            "INSERT INTO channels (id, type, name) VALUES ($1, $2, $3) RETURNING *;",
                            meta.create_snowflake(),
                            0,
                            None,
                        )
                    )
                    bulk_add_channel_members = await session.prepare(
                        "INSERT INTO channel_members (channel_id, user_id) VALUES ($1, $2);"
                    )

                    m1 = await bulk_add_channel_members.fetchrow(
                        channel["id"], user["id"]
                    )
                    m2 = await bulk_add_channel_members.fetchrow(
                        channel["id"], target["id"]
                    )
                    channel["recipients"] = [dict(m1), dict(m2)]  # type: ignore

                    await meta.publish_channel(
                        "CHANNEL_CREATE", [user["id"], target["id"]], channel
                    )

        return dict(relationship)
