import os
import random
import time
from typing import Optional

import uvicorn
from fastapi import FastAPI, Depends, status, Response
from sqlalchemy.exc import IntegrityError

from app.core.deps import get_user_repository
from app.middleware.prometheus import metrics, PrometheusMiddleware
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserInfo, User, UserUpdate

APP_NAME = os.environ.get("APP_NAME")

app = FastAPI()
app.add_middleware(PrometheusMiddleware, app_name=APP_NAME)
app.add_route("/metrics", metrics)


config = {
    'DB_NAME': os.environ.get('DB_NAME', 'user-db'),
    'DB_HOST': os.environ['DB_HOST'],
    'DB_PORT': os.environ['DB_PORT'],
    'GREETING': os.environ.get('GREETING', 'Hello'),
}


@app.get('/')
async def root():
    return {"message": "Hi there"}


@app.get('/health')
async def check_health():
    return {"status": "OK"}


@app.get("/random_status")
async def random_status(response: Response):
    response.status_code = random.choice([200, 200, 300, 400, 500, 501, 502, 503])
    return {"path": "/random_status"}


@app.get("/random_sleep")
async def random_sleep(response: Response):
    time.sleep(random.randint(0, 200) * 0.001)
    return {"path": "/random_sleep"}


@app.post('/user', response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
        user_info: UserInfo,
        response: Response,
        user_repository: UserRepository = Depends(get_user_repository),
):
    try:
        return await user_repository.create_user(
            user_name=user_info.user_name,
            first_name=user_info.first_name,
            last_name=user_info.last_name,
            email=user_info.email
        )
    except IntegrityError:
        response.status_code = status.HTTP_409_CONFLICT


@app.get('/user/{user_id}', response_model=Optional[User])
async def get_user_by_id(
        user_id: int,
        response: Response,
        user_repository: UserRepository = Depends(get_user_repository),
):
    user = await user_repository.get_user_by_id(
        user_id=user_id
    )

    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND

    return user


@app.delete('/user/{user_id}', response_model=Optional[User])
async def get_user_by_id(
        user_id: int,
        response: Response,
        user_repository: UserRepository = Depends(get_user_repository),
):
    user = await user_repository.delete_user(
        user_id=user_id
    )

    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND

    return user


@app.put('/user/{user_id}', response_model=Optional[User])
async def update_user_by_id(
        user_id: int,
        user_update: UserUpdate,
        response: Response,
        user_repository: UserRepository = Depends(get_user_repository),
):
    user = await user_repository.update_user(
        user_id=user_id,
        first_name=user_update.first_name,
        last_name=user_update.last_name,
        email=user_update.email
    )

    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND

    return user


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, log_level="info")