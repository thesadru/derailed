from asyncpg.pool import PoolConnectionProxy

from ..error import Error


async def get_channel(channel_id: int, user_id: int, session: PoolConnectionProxy):
    channel = await session.fetchrow(
        "SELECT * FROM channels WHERE id = $1 AND id IN (SELECT channel_id FROM channel_members WHERE user_id = $2);",
        channel_id,
        user_id,
    )

    if channel is None:
        raise Error(4004, "Channel does not exist", 404)

    return dict(channel)
