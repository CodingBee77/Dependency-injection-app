from app.models import Item
from app.schemas import ItemCreate


class ItemRepository():
    def __init__(self, session_factory):
        self.session_factory = session_factory
    

    def get_items(self, skip: int = 0, limit: int = 100):
        with self.session_factory() as session:
            return session.query(Item).offset(skip).limit(limit).all()


    def create_user_item(self, obj_in: ItemCreate, user_id: int)-> Item:
        with self.session_factory() as session:
            db_item = Item(**obj_in.dict(), owner_id=user_id)
            session.add(db_item)
            session.commit()
            session.refresh(db_item)
            return db_item
