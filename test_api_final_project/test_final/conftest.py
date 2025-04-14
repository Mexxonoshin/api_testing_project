import pytest
from test_api_final_project.final_endpoints.auth import Auth
from test_api_final_project.final_endpoints.get_mem import GetMem
from test_api_final_project.final_endpoints.post_mem import PostMem
from test_api_final_project.final_endpoints.put_meme import PutMem
from test_api_final_project.final_endpoints.delete_meme import DeleteMem
from test_api_final_project.final_endpoints.core import CoreAPI


@pytest.fixture
def auth_client():
    """Фикстура для тестов авторизации"""
    client = Auth()
    yield client
    # Автоматическая очистка токена после теста
    client.headers.pop('Authorization', None)

@pytest.fixture
def authorized_client(auth_client):
    """Фикстура для авторизованного клиента"""
    auth_client.authorize("ARTEW")
    return auth_client

@pytest.fixture
def mem_client(authorized_client):
    """Фикстура для работы с мемами уже авторизованного клиента"""
    client = GetMem()
    client.headers['Authorization'] = authorized_client.headers['Authorization']
    yield client
    # Автоматическая очистка токена после теста
    client.headers.pop('Authorization', None)

@pytest.fixture
def unauthorized_mem_client():
    """Фикстура для работы с мемами без авторизации"""
    client = GetMem()
    yield client
    # Автоматическая очистка токена после теста
    client.headers.pop('Authorization', None)

@pytest.fixture
def core_client():
    """Фикстура для системных эндпоинтов API"""
    client = CoreAPI()
    yield client


@pytest.fixture
def post_client(authorized_client):
    """Фикстура для создания мемов (авторизованная)"""
    client = PostMem()
    client.headers['Authorization'] = authorized_client.headers['Authorization']
    yield client
    client.headers.pop('Authorization', None)

@pytest.fixture
def unauthorized_post_client():
    """Фикстура для создания мемов без авторизации"""
    client = PostMem()
    yield client
    client.headers.pop('Authorization', None)

@pytest.fixture
def put_client(authorized_client):
    """Фикстура для обновления мемов (авторизованная)"""
    client = PutMem()
    client.headers['Authorization'] = authorized_client.headers['Authorization']
    yield client
    client.headers.pop('Authorization', None)

@pytest.fixture
def unauthorized_put_client():
    """Фикстура для обновления мемов без авторизации"""
    client = PutMem()
    yield client
    # Автоматическая очистка токена после теста
    client.headers.pop('Authorization', None)


@pytest.fixture()
def unauthorized_delete_client():
    """Фикстура для удаления мемов"""
    client = DeleteMem()
    yield client
    # Автоматическая очистка токена после теста
    client.headers.pop('Authorization', None)

@pytest.fixture
def delete_client(authorized_client):
    """Фикстура для обновления мемов (авторизованная)"""
    client = DeleteMem()
    client.headers['Authorization'] = authorized_client.headers['Authorization']
    yield client
    client.headers.pop('Authorization', None)
