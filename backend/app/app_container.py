from dependency_injector import containers, providers

from app.database import Database

from app.repositories.item_repository import ItemRepository
from app.repositories.user_repository import UserRepository
from app.service import ItemService, UserService


class Databases(containers.DeclarativeContainer):
    """

    Singleton provider provides single object.
    It memorizes the first created object and returns it
    on the rest of the calls.
    """

    config = providers.Configuration()

    db_provider = providers.Singleton(Database, db_url="sqlite:///./app.db")


class Users(containers.DeclarativeContainer):

    config = providers.Configuration()
    databases = providers.DependenciesContainer()

    user_repo = providers.Factory(
        UserRepository,
        session_factory=databases.db_provider.provided.session,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repo,
    )


class Items(containers.DeclarativeContainer):

    config = providers.Configuration()
    databases = providers.DependenciesContainer()

    item_repo = providers.Factory(
        ItemRepository,
        session_factory=databases.db_provider.provided.session,
    )

    item_service = providers.Factory(
        ItemService,
        item_repository=item_repo,
    )


class Application(containers.DeclarativeContainer):

    config = providers.Configuration()

    databases = providers.Container(Databases, config=config.databases)

    user = providers.Container(Users, config=config.users, databases=databases)
    item = providers.Container(Items, config=config.items, databases=databases)
