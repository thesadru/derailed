from typing import Annotated
import argon2
from fastapi import APIRouter, Request
import itsdangerous
import pydantic
import asyncpg.exceptions

from ..factors.user_factors import get_user_from_token

from ..missing import MISSING, Maybe

from ..error import Error

from ..meta import meta

router = APIRouter()
db = meta.db
pwhasher = argon2.PasswordHasher()

class Register(pydantic.BaseModel):
    email: Annotated[str, pydantic.Field(min_length=5, max_length=128)]
    username: Annotated[str, pydantic.Field(min_length=3, max_length=32)]
    password: Annotated[str, pydantic.Field(min_length=8, max_length=128)]


@router.post("/register")
async def register(model: Register):
    async with db.acquire() as session:
        try:
            user_rec = await session.fetchrow(
                "INSERT INTO users id, email, username, password VALUES ($1, $2, $3, $4) RETURNING *;",
                model.email,
                model.username,
                pwhasher.hash(model.password)
            )
        except asyncpg.exceptions.UniqueViolationError:
            raise Error(1000, "username or email must be unique")

        assert user_rec is not None

        user = dict(user_rec)

        signer = itsdangerous.TimestampSigner(user.pop("password"))

        user["_token"] = signer.sign(user["id"])

        return user

class PatchUser(pydantic.BaseModel):
    email: Annotated[Maybe[str], pydantic.Field(MISSING, min_length=5, max_length=128)]
    username: Annotated[Maybe[str], pydantic.Field(MISSING, min_length=3, max_length=32)]
    password: Annotated[Maybe[str], pydantic.Field(MISSING, min_length=8, max_length=128)]

@router.patch("/users/@me")
async def modify_user(request: Request, model: PatchUser):
    async with db.acquire() as session:
        user = await get_user_from_token(request, session)

        async with session.transaction():
            if model.email:
                if model.email != user["email"]:
                    user["email"] = model.email
                    await session.execute("UPDATE users SET email = $1 WHERE id = $2;", model.email, user['id'])
            if model.username:
                if model.username != user["username"]:
                    user["username"] = model.username
                    try:
                        await session.execute("UPDATE users SET username = $1 WHERE id = $2", model.username, user["id"])
                    except asyncpg.UniqueViolationError:
                        raise Error(1000, "username or email must be unique")
            if model.password:
                await session.execute("UPDATE users SET password = $1 WHERE id = $2", pwhasher.hash(model.password), user["id"])

        return user
