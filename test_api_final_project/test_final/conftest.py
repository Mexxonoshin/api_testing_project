import pytest
import random
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

@pytest.fixture
def create_meme_for_update(post_client):
    """Фикстура создает тестовый мем для проверки обновления"""
    test_data = {
        "text": "Test meme for unauthorized update",
        "url": "https://example.com/test.jpg",
        "tags": ["test"],
        "info": {"author": "test"}
    }
    post_client.create_meme(**test_data)
    post_client.check_status(200)
    meme_id = post_client.response.json()["id"]
    yield meme_id

@pytest.fixture
def other_user_delete_client(auth_client, delete_client):
    """Фикстура для клиента удаления с авторизацией другого пользователя"""
    auth_client.authorize("OTHER-user")
    delete_client.headers['Authorization'] = auth_client.token
    yield delete_client
    delete_client.headers.pop('Authorization', None)

@pytest.fixture
def existing_meme_id(mem_client):
    """Фикстура возвращает ID существующего мема"""
    mem_client.get_all_memes()
    mem_client.check_status(200)
    all_memes = mem_client.check_json_response()
    return all_memes['data'][0]['id']


@pytest.fixture
def nonexistent_meme_id(mem_client):
    """Фикстура генерирует и проверяет несуществующий ID мема"""
    while True:
        # Генерируем случайный ID в большом диапазоне
        random_id = random.randint(100000, 999999)

        # Проверяем, существует ли мем с таким ID
        mem_client.get_meme_by_id(random_id)
        if mem_client.response.status_code == 404:
            yield random_id
            break