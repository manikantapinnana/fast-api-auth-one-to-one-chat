from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.schemas.user import Token, UserInCreate, UserInLogin, UserInResponse
from app.service.userservice import UserService

auth_router = APIRouter()


@auth_router.post("/register", response_model=UserInResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserInCreate, db: Session = Depends(get_db)) -> UserInResponse:
    return UserService(db).create_user(user)


@auth_router.post("/login", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    # OAuth2PasswordRequestForm provides 'username' and 'password' fields.
    login_data = UserInLogin(email=form_data.username, password=form_data.password)
    return UserService(db).login_user(login_data)
