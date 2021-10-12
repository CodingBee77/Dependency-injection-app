from app.models import User
from app.schemas import UserCreate


class UserRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def get_user_by_id(self, user_id: int):
        with self.session_factory() as session:
            return session.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str):
        with self.session_factory() as session:
            return session.query(User).filter(User.email == email).first()

    def get_users(self, skip: int = 0, limit: int = 100):
        with self.session_factory() as session:
            return session.query(User).offset(skip).limit(limit).all()

    def create_user(self, user: UserCreate):
        with self.session_factory() as session:
            db_user = User(email=user.email)
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user
