import asyncio

import websockets.server as websockets

from .session import Session


async def ws_handler(ws: websockets.WebSocketServerProtocol):
    session = Session(ws)
    await session.run()


async def main():
    async with websockets.serve(
        ws_handler,
        "0.0.0.0:15000"
    ):
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())