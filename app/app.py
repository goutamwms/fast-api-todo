from fastapi import FastAPI, Depends
from app.routing import todo, auth, demo
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
from app.config.app_config import getAppConfig

# from app.database.db import Base, engine

app = FastAPI()
load_dotenv()

# Base.metadata.create_all(bind=engine)

app.include_router(todo.router)
app.include_router(auth.router)
app.include_router(demo.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    # return JSONResponse(
    #     status_code=400, content={"detail": exc.errors(), "body": exc.body}
    # )

    errors = {}

    for error in exc.errors():
        print(f"the error is {error}")
        errors[error["loc"][-1]] = error["msg"]

    # custom JSONResponse
    return JSONResponse(
        {"message": "Validation error", "errors": errors},
        status_code=422,
    )


@app.get("/")
def root():
    config = getAppConfig()
    return {
        "message": "hello",
        "app_name": os.getenv("APP_NAME"),
        "app_env": config.app_env,
    }
