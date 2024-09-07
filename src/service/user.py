from src.client.database import DBClient
from src.db.user import User
from src.schema.user import UserCreateRequest, UserResponse


class UserService:

    @classmethod
    def create_user(cls, request: UserCreateRequest, db_client: DBClient):
        db_client.query(
            User.add,
            items=[
                User(
                    email=request.email,
                    name=request.name,
                    firebase_user_id=request.firebase_user_id,
                )
            ],
        )

    @classmethod
    def get_user(cls, user: User) -> UserResponse:
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
        )
