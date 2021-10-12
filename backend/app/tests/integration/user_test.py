from unittest import mock
import pytest

from app.repositories.user_repository import UserRepository
from app.main import app
from app.tests.utils.model_factory import UserFactory, ItemFactory
from fastapi.testclient import TestClient
from . import common

from dependency_injector.wiring import inject, Provide


def item_to_str(item):
    return {"id": item.id, "title": item.title, "owner_id": item.owner_id}



class MyTest(fastapi.testclient.TestClient):

    def setUp(self):
        # Prepare a new, clean session
        self.session = common.Session()


    @pytest.fixture
    def client(self):
        yield TestClient(app)


    @inject
    def test_get_users(self, client):
        repository_mock = mock.Mock(spec=UserRepository)

        item1 = ItemFactory()
        item2 = ItemFactory()
        item3 = ItemFactory()
        
        user = UserFactory.create(items=(item1, item2, item3))

        print(f"this is a user from a factory {user.id, user.email, user.is_active, user.items}")
        
        repository_mock.get_users.return_value = [user]

        with app.container.user.user_repo.override(repository_mock):
            response = client.get("/users")

        assert response.status_code == 200
        data = response.json()
        assert data == [
            {
                "id": user.id,
                "email": user.email,
                "is_active": user.is_active,
                "items": [item_to_str(item) for item in user.items],
            }
        ]


    def tearDown(self):
        # Rollback the session => no changes to the database
        self.session.rollback()
        # Remove it, so that the next test gets a new Session()
        common.Session.remove()






# @inject
# def test_get_by_id(client):
#     repository_mock = mock.Mock(spec=UserRepository)
#     item1 = ItemFactory()
#     item2 = ItemFactory()
    
#     user = UserFactory.create(items=(item1, item2))

    
    
#     repository_mock.get_user_by_id.return_value = [user]
    

#     with app.container.user.user_repo.override(repository_mock):
#         response = client.get("/users/1")

#     assert response.status_code == 200
#     data = response.json()
#     assert data == {"id": 1, "email": "xyz@email.com", "is_active": True, "items": []}
#     repository_mock.get_user_by_id.assert_called_once_with(1)


# def test_get_by_id_404(client):
#     repository_mock = mock.Mock(spec=UserRepository)
#     repository_mock.get_by_id.side_effect = UserNotFoundError(1)

#     with app.container.user_repository.override(repository_mock):
#         response = client.get('/users/1')

#     assert response.status_code == 404


# @mock.patch('webapp.services.uuid4', return_value='xyz')
# def test_add(_, client):
#     repository_mock = mock.Mock(spec=UserRepository)
#     repository_mock.add.return_value = User(
#         id=1,
#         email='xyz@email.com',
#         hashed_password='pwd',
#         is_active=True,
#     )

#     with app.container.user_repository.override(repository_mock):
#         response = client.post('/users')

#     assert response.status_code == 201
#     data = response.json()
#     assert data == {'id': 1, 'email': 'xyz@email.com', 'hashed_password': 'pwd', 'is_active': True}
#     repository_mock.add.assert_called_once_with(email='xyz@email.com', password='pwd')


# def test_remove(client):
#     repository_mock = mock.Mock(spec=UserRepository)

#     with app.container.user_repository.override(repository_mock):
#         response = client.delete('/users/1')

#     assert response.status_code == 204
#     repository_mock.delete_by_id.assert_called_once_with(1)


# def test_remove_404(client):
#     repository_mock = mock.Mock(spec=UserRepository)
#     repository_mock.delete_by_id.side_effect = UserNotFoundError(1)

#     with app.container.user_repository.override(repository_mock):
#         response = client.delete('/users/1')

#     assert response.status_code == 404
