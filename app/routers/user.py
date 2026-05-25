from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security.authhandler import get_current_user
from app.db.schemas.user import UserDeleteResponse, UserInResponse, UserInUpdate
from app.service.userservice import UserService

user_router = APIRouter()

@user_router.get("/me", response_model=UserInResponse)
async def read_current_user(current_user: UserInResponse = Depends(get_current_user)) -> UserInResponse:
    return current_user

@user_router.delete("/{user_id}", response_model=UserDeleteResponse)
async def delete_user(user_id: int, db: Session = Depends(get_db)) -> UserDeleteResponse:
    return UserService(db).delete_user(user_id)

@user_router.put("/update", response_model=UserInResponse)
async def update_user(user_data: UserInUpdate, db: Session = Depends(get_db)) -> UserInResponse:
    return UserService(db).update_user(user_data)
    
@user_router.get("/{user_id}", response_model=UserInResponse)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)) -> UserInResponse:
    return UserService(db).get_user_by_id(user_id)

@user_router.get("/", response_model=list[UserInResponse])
async def get_all_users(db: Session = Depends(get_db)) -> list[UserInResponse]:
    return UserService(db).get_all_users()

@user_router.post("/{user_id}/upload", response_model=dict)
async def upload_file(user_id: int, file: UploadFile, db: Session = Depends(get_db)):
    print(f"Received file: {file.filename} for user_id: {user_id}. File size is {file.size} bytes.")
    return UserService(db).upload_file_for_user(user_id, file)

# router -> service -> repository -> db
# router <- service <- repository <- db

