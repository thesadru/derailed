from fastapi import FastAPI, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from derailed_api.error import Error

from .meta import meta
from .routers import messages, users

app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
app.include_router(users)
app.include_router(messages)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await meta.start()
    yield
    await meta.db.close()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_req: Request, exc: RequestValidationError):
    return JSONResponse(
        {
            "code": 0,
            "message": "Invalid data",
            "_errors": jsonable_encoder(exc.errors()),
        }
    )


@app.exception_handler(Error)
async def default_error_exception_handler(_req: Request, exc: Error):
    return JSONResponse(exc.to_json(), exc.status_code)


@app.exception_handler(500)
async def internal_error_exception_handler(_req: Request, _exc: Exception):
    return JSONResponse({"code": 0, "message": "Internal server error"}, 500)
