from typing import Annotated, Literal, TypedDict

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
db = meta.db
pwhasher = argon2.PasswordHasher()


class Register(pydantic.BaseModel):
    email: pydantic.EmailStr
    username: Annotated[str, pydantic.Field(min_length=3, max_length=32, pattern=r"^[a-z0-9]+(?:[._][a-z0-9]+)*$")]
    password: Annotated[str, pydantic.Field(min_length=8, max_length=128)]


@router.post("/register")
async def register(model: Register):
    async with db.acquire() as session:
        async with session.transaction():
            try:
                user_rec = await session.fetchrow(
                    "INSERT INTO users (id, email, username, password VALUES) VALUES ($1, $2, $3, $4) RETURNING *;",
                    meta.create_snowflake(),
                    model.email.lower(),
                    model.username.lower(),
                    pwhasher.hash(model.password),
                )
            except asyncpg.exceptions.UniqueViolationError:
                raise Error(1000, "username or email must be unique")

            assert user_rec is not None

            await session.fetchrow("INSERT INTO user_settings (user_id) VALUES ($1);", user_rec["id"])

            user = dict(user_rec)

            signer = itsdangerous.TimestampSigner(user.pop("password"))

            user["_token"] = signer.sign(user["id"])

        return user


class Login(pydantic.BaseModel):
    email: Annotated[str, pydantic.Field(min_length=5, max_length=128)]
    password: Annotated[str, pydantic.Field(min_length=8, max_length=128)]


@router.post("/login")
async def login(model: Login):
    async with db.acquire() as session:
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
    async with db.acquire() as session:
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
    type: Literal[1, 3, None]


@router.put("/users/by-username/{username}/relationship")
async def put_relationship(request: Request, username: str, model: RelationshipType):
    async with db.acquire() as session:
        user = await get_user_from_token(request, session)
        target = await session.fetchrow("SELECT * FROM users WHERE username = $1;", username.lower())
        assert target is not None

        target_user_relation = await session.fetchval("SELECT relation FROM relationships WHERE origin_user_id = $1 AND target_user_id = $2;", target['id'], user['id'])

        if target_user_relation == 1 and model.type != None:
            raise Error(1002, "User has blocked you")

        await session.fetch("DELETE FROM relationships WHERE origin_user_id = $1 AND target_user_id = $2;", user["id"], target["id"])

        if model.type == None:
            return ""

        relationship = await session.fetchrow("INSERT INTO relationships (origin_user_id, target_user_id, relation) VALUES ($1, $2, $3)", user["id"], target["id"], model.type)
        assert relationship is not None

        return dict(relationship)
