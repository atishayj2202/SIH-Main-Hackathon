from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from src.client.database import DBClient
from src.schema.user import UserCreateRequest
from src.utils.client import getDBClient

USER_PREFIX = "/user"
user_router = APIRouter(prefix=USER_PREFIX)

CREATE_USER = "/create-user/"


@user_router.post(CREATE_USER)
async def create_user(
    request: UserCreateRequest, db_client: DBClient = Depends(getDBClient)
):
    UserService.createUser(request, db_client)
    return Response(status_code=status.HTTP_200_OK)
