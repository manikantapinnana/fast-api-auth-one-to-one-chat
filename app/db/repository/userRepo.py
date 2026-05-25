from app.db.models.user import User
from app.db.repository.base import BaseRepository
from app.db.schemas.user import UserInCreate, UserInUpdate


class UserRepository(BaseRepository):
    def create_user(self, user_data: UserInCreate):
        newUser = User(**user_data.model_dump(exclude_none=True))
        self.session.add(newUser)
        self.session.commit()
        self.session.refresh(newUser)
        return newUser
    def user_exists_by_email(self, email: str):
        user = self.session.query(User).filter(User.email == email).first()
        return bool(user)
    def get_user_by_email(self, email: str):
        user = self.session.query(User).filter(User.email == email).first()
        return user
    def get_user_by_id(self, user_id: int):
        user = self.session.query(User).filter(User.id == user_id).first()
        return user
    def delete_user_by_id(self, user_id: int):
        user = self.session.query(User).filter(User.id == user_id).first()
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False
    def update_user(self, user_data: UserInUpdate):
        user = self.session.query(User).filter(User.id == user_data.id).first()
        if not user:
            return None
        for field, value in user_data.model_dump(exclude_none=True).items():
            setattr(user, field, value)
        self.session.commit()
        self.session.refresh(user)
        return user
    def get_all_users(self):
        users = self.session.query(User).all()
        return users