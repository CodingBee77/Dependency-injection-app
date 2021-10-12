import factory
from factory import LazyAttribute
from app.models import User, Item
from app.tests import common


class ItemFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Item
        sqlalchemy_session = common.Session

    id = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: "Title %d" % n)
    owner_id = LazyAttribute(lambda a: UserFactory().id)


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = common.Session

    id = factory.Sequence(lambda n: n)
    email = factory.Sequence(lambda n: "john%d@hotmail.com" % n)
    # TODO: check how to change it to random bool
    is_active = True


    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for item in extracted:
                self.items.append(item)