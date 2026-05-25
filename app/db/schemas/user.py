from pydantic import BaseModel, EmailStr, constr


PasswordStr = constr(min_length=8)


class UserInCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: PasswordStr


class UserInResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserInLogin(BaseModel):
    email: EmailStr
    password: PasswordStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: str | None = None


class UserDeleteResponse(BaseModel):
    message: str


class UserInUpdate(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    password: PasswordStr | None = None
