import os
import asyncpg


class Meta:
    def __init__(self):
        self.db: asyncpg.Pool[asyncpg.Record]

    async def start(self) -> None:
        self.db = await asyncpg.create_pool(os.getenv("PG_DSN"), record_class=Record) # type: ignore


meta = Meta()
