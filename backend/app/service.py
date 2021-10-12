from app.schemas import UserCreate, ItemCreate
from app.repositories.user_repository import UserRepository
from app.repositories.item_repository import ItemRepository
from app.models import User, Item
from typing import Iterator

class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._repository = user_repository

    def get_users(self, skip, limit) -> Iterator[User]:
        return self._repository.get_users(skip=skip, limit=limit)

    def get_user_by_id(self, user_id: int) -> User:
        return self._repository.get_user_by_id(user_id)
    
    def get_user_by_email(self, email: str) -> User:
        return self._repository.get_user_by_email(email)
    
    def create_user(self, obj_in: UserCreate) -> User:
        return self._repository.create_user(obj_in)
    
    
class ItemService:
    def __init__(self, item_repository: ItemRepository) -> None:
        self._repository: ItemRepository = item_repository

    def get_items(self, skip, limit) -> Iterator[Item]:
        return self._repository.get_items(skip=skip, limit=limit)
    
    def create_item(self, obj_in: ItemCreate, user_id: int) -> User:
        return self._repository.create_user_item(obj_in, user_id)
    
    
    
    