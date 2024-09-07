from fastapi import Depends, Header, HTTPException
from pydantic import BaseModel
from starlette import status

from src.auth.base import _get_requesting_user
from src.client.database import DBClient
from src.client.firebase import FirebaseClient
from src.db.user import User
from src.utils.client import getDBClient, getFirebaseClient


class VerifiedUser(BaseModel):
    requesting_user: User


def verify_user(
    authorization: str = Header(...),
    cockroach_client: DBClient = Depends(getDBClient),
    firebase_client: FirebaseClient = Depends(getFirebaseClient),
) -> VerifiedUser:
    user: User = _get_requesting_user(authorization, cockroach_client, firebase_client)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return VerifiedUser(requesting_user=user)
