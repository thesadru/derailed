import os
import threading
import time
from typing import Any

import asyncpg
import grpc.aio as grpc
import msgspec
import redis.asyncio as redis

from .gateway import GatewayStub, Interchange


class Meta:
    def __init__(self):
        self.db: asyncpg.Pool[asyncpg.Record]
        self._incr = 0

    async def start(self) -> None:
        self.db = await asyncpg.create_pool(os.getenv("PG_DSN"), record_class=Record)  # type: ignore
        self.curthread = threading.current_thread().ident
        self.pid = os.getpid()
        self.grpc = GatewayStub(
            grpc.insecure_channel(os.environ["GATEWAY_GRPC_CHANNEL"])
        )
        self.redis = redis.from_url(os.getenv("REDIS_URI") or "error")

    async def publish_channel(
        self, type: str, user_ids: list[int], data: dict[str, Any]
    ) -> None:
        await self.redis.publish(
            "channels",
            msgspec.json.encode(
                {"type": "CHANNEL_EVENT", "t": type, "d": data, "to": user_ids}
            ),
        )

    async def publish_user(self, type: str, user_id: int, data: dict[str, Any]) -> None:
        await self.redis.publish(
            "users",
            msgspec.json.encode(
                {"type": "USER_EVENT", "t": type, "d": data, "to": user_id}
            ),
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
