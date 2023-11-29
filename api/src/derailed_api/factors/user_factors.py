import base64
import binascii
from typing import Any
from asyncpg.pool import PoolConnectionProxy
from fastapi import Request
from itsdangerous import TimestampSigner
from ..error import Error


async def get_user_from_token(request: Request, session: PoolConnectionProxy):
    auth = request.headers.get("Authorization")

    if auth is None:
        raise Error(1001, "Authorization header not present", 401)

    try:
        fragmented = auth.split(".")
        enc_id = fragmented[0]
        user_id = int(base64.b64decode(enc_id.encode()).decode())
    except (IndexError, binascii.Error, UnicodeDecodeError, ValueError):
        raise Error(1003, "Invalid token", 401)

    user: dict[str, Any] = dict(await session.fetchrow("SELECT * FROM users WHERE id = $1", user_id)) # type: ignore

    if user is None:
        raise Error(1004, "Token is no longer valid", 401)

    signer = TimestampSigner(user.pop("password"))

    if not signer.validate(auth):
        raise Error(1003, "Invalid Token", 401)

    return user
