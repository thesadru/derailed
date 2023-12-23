import asyncio
import os
import threading
import time
import typing
from typing import Any, Literal, cast

import asyncpg
import msgspec
import redis.asyncio as redis

if typing.TYPE_CHECKING:
    from .session import Session


class ChannelData:
    type: Literal["CHANNEL_EVENT"]
    t: str
    d: Any
    to: list[int]


class UserData:
    type: Literal["USER_EVENT"]
    t: str
    d: Any
    to: int


class Meta:
    def __init__(self):
        self.db: asyncpg.Pool[asyncpg.Record]
        self._incr = 0
        self._recv_task = None
        self.sessions: list["Session"] = []

    async def start(self) -> None:
        self.db = await asyncpg.create_pool(os.getenv("PG_DSN"), record_class=Record)  # type: ignore
        self.curthread = threading.current_thread().ident
        self.pid = os.getpid()
        self.redis = redis.from_url(os.getenv("REDIS_URI") or "error")
        self.pubsub = self.redis.pubsub()
        self._recv_task = asyncio.create_task(self.recv())

    async def recv(self) -> None:
        await self.pubsub.subscribe("channels", "users")
        while True:
            msg = await self.pubsub.get_message(timeout=None)  # type: ignore

            data: dict[str, Any] = msgspec.json.decode(msg)
            receivers = cast(list[int] | int, data.pop("to"))

            if not isinstance(receivers, list):
                receivers = [receivers]

            for session in self.sessions:
                if session.user_id in receivers:
                    await session.send(data)

    def create_snowflake(self) -> int:
        current_ms = int(time.time() * 1000)
        epoch = current_ms - 1672531200000 << 22

        if self.curthread is None:
            raise AssertionError

        epoch |= (self.curthread % 32) << 17
        epoch |= (self.pid % 32) << 12

        epoch |= self._incr % 4096

        if self._incr == 9000000000:
            self._incr = 0

        self._incr += 1

        return epoch


meta = Meta()
