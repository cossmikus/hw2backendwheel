from typing import Any
from fastapi import Depends
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class CreateTweetRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


class CreateTweetResponse(AppModel):
    id: Any = Field(alias="_id")


@router.post("/", response_model=CreateTweetResponse)
def create_tweet(
    input: CreateTweetRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    tweet_id = svc.repository.create_tweet_rep(jwt_data.user_id, input.dict())
    return CreateTweetResponse(id=tweet_id, content="OK")
