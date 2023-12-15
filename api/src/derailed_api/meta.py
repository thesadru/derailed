import os
import time
import threading
from typing import Any

import asyncpg
import msgspec
import grpc.aio as grpc

from .gateway import GatewayStub, Interchange


class Meta:
    def __init__(self):
        self.db: asyncpg.Pool[asyncpg.Record]
        self._incr = 0

    async def start(self) -> None:
        self.db = await asyncpg.create_pool(os.getenv("PG_DSN"), record_class=Record)  # type: ignore
        self.curthread = threading.current_thread().ident
        self.pid = os.getpid()
        self.grpc = GatewayStub(grpc.insecure_channel(os.environ["GATEWAY_GRPC_CHANNEL"]))

    async def publish_guild(
        self, type: str, guild_id: int, data: dict[str, Any]
    ) -> None:
        await self.grpc.dispatch_guild(
            Interchange(
                t=type,
                id=guild_id,
                d=msgspec.json.encode(data).decode()
            )
        )

    async def publish_user(
        self, type: str, user_id: int, data: dict[str, Any]
    ) -> None:
        await self.grpc.dispatch_user(
            Interchange(
                t=type,
                id=user_id,
                d=msgspec.json.encode(data).decode()
            )
        )

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
