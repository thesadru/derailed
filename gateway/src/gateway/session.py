import asyncio
import base64
import binascii
from typing import Any
from itsdangerous import TimestampSigner
import msgspec
from pydantic import BaseModel
import websockets.server as websockets

from api.src.derailed_api import meta


async def authorize(auth: str) -> dict[str, Any] | None:
    try:
        fragmented = auth.split(".")
        enc_id = fragmented[0]
        user_id = int(base64.b64decode(enc_id.encode()).decode())
    except (IndexError, binascii.Error, UnicodeDecodeError, ValueError):
        return None

    async with meta.db.acquire() as session:
        user: dict[str, Any] = dict(await session.fetchrow("SELECT * FROM users WHERE id = $1", user_id))  # type: ignore

    if user is None:
        return None

    signer = TimestampSigner(user.pop("password"))

    if not signer.validate(auth):
        return None

    return dict(user)


class Identify(BaseModel):
    token: str


class Session:
    # WS Codes
    PAYLOAD_INVALID = 2000
    INVALID_AUTHORIZATION = 2001
    ALREADY_AUTHORIZED = 2002

    # Op Codes
    EVENT = 0
    HELLO = 1
    IDENTIFY = 2

    def __init__(self, ws: websockets.WebSocketServerProtocol) -> None:
        self.ws = ws
        self.user = {}
        self.user_id: int = 0
        self.identified = False
        self._recv_fut = None
        self._future = asyncio.Future()

    async def send(self, data: dict[str, Any]) -> None:
        await self.ws.send(msgspec.json.encode(data))

    async def stop(self, code: int, reason: str) -> None:
        await self.ws.close(code, reason)
        self._future.set_result(None)

    async def _recv(self) -> None:
        async for msg in self.ws:
            try:
                data = msgspec.json.decode(msg)
            except msgspec.DecodeError:
                await self.stop(self.PAYLOAD_INVALID, "Payload is invalid")
                break

            if "op" not in data:
                await self.stop(self.PAYLOAD_INVALID, "Payload is invalid (Op Code not present)")
                break

            if data["op"] == self.IDENTIFY:
                if self.identified:
                    await self.stop(self.ALREADY_AUTHORIZED, "Connection is already authorized")
                    break

                identify = Identify.model_validate(data)

                token = identify.token

                user = await authorize(token)

                if user is None:
                    await self.stop(self.INVALID_AUTHORIZATION, "Authorization is invalid")
                    break

                self.user_id = user["id"]
                self.user = user

                # collect ready data
                async with meta.db.acquire() as session:
                    relationships_rec = await session.fetch(
                        "SELECT relation, target_user_id FROM relationships WHERE origin_user_id = $1;",
                        user["id"]
                    )
                    relationships = []
                    for r in relationships_rec:
                        relationships.append(dict(r))

                    memberships = await session.fetch("SELECT channel_id FROM channel_members WHERE user_id = $1;", user["id"])

                    channels = []

                    for m in memberships:
                        channels.append(dict(await session.fetchrow("SELECT * FROM channels WHERE id = $1;", m["channel_id"]))) # type: ignore

                await self.send({
                    'op': 0,
                    't': "READY",
                    'd': {
                        "user": user,
                        "relationships": relationships,
                        "channels": channels
                    }
                })
            else:
                await self.stop(self.PAYLOAD_INVALID, "Invalid Op Code provided")
                break

    async def run(self) -> None:
        self._recv_fut = asyncio.create_task(self._recv())
        await self._future
