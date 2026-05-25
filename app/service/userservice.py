from sqlalchemy.orm import Session
from app.core.security.authhandler import create_access_token
from app.core.security.hashhelper import hash_password, verify_password
from app.db.repository.userRepo import UserRepository
from app.db.schemas.user import Token, UserDeleteResponse, UserInCreate, UserInLogin, UserInResponse, UserInUpdate
from fastapi import HTTPException, status


class UserService:
    def __init__(self, session: Session):
        self.__userRepository = UserRepository(session)

    def create_user(self, user_data: UserInCreate) -> UserInResponse:
        if self.__userRepository.user_exists_by_email(user_data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")
        try:
            hashed_password = hash_password(user_data.password)
        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Password hashing failed") from exc

        user_payload = user_data.dict()
        user_payload["password"] = hashed_password
        user_data_hashed = UserInCreate(**user_payload)

        return self.__userRepository.create_user(user_data_hashed)

    def authenticate_user(self, email: str, password: str):
        user = self.__userRepository.get_user_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def login_user(self, login_data: UserInLogin) -> Token:
        user = self.authenticate_user(login_data.email, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(data={"sub": user.email})
        return Token(access_token=access_token, token_type="bearer")

    def delete_user(self, user_id:int) -> UserDeleteResponse:
        if not self.__userRepository.get_user_by_id(user_id=user_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        self.__userRepository.delete_user_by_id(user_id=user_id)
        return UserDeleteResponse(message="User deleted successfully")

    def update_user(self, user_data: UserInUpdate) -> UserInResponse:
        existing_user = self.__userRepository.get_user_by_id(user_id=user_data.id)
        if not existing_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if user_data.email and user_data.email != existing_user.email and self.__userRepository.user_exists_by_email(user_data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")

        update_payload = user_data.dict(exclude_none=True)
        if update_payload.get("password"):
            try:
                update_payload["password"] = hash_password(update_payload["password"])
            except Exception as exc:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Password hashing failed") from exc
        user_data_hashed = UserInUpdate(**update_payload)
        return self.__userRepository.update_user(user_data_hashed)

    def get_user_by_id(self, user_id: int) -> UserInResponse:
        user = self.__userRepository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    def get_all_users(self) -> list[UserInResponse]:
        users = self.__userRepository.get_all_users()
        return users
