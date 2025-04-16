import allure
import pytest
import requests


@allure.title("GET / - Проверка главной страницы API")
def test_welcome_page(core_client):
    response = core_client.check_welcome_page()
    print(f"Ответ сервера: {response.text}")


@allure.title("Авторизация с массивом вместо имени")
def test_auth_with_array_instead_of_name(auth_client):
    # Отправляем невалидные данные (используем правильное имя метода)
    auth_client.authorize_invalid(json_data={"name": []})
    auth_client.check_status(400)
    auth_client.check_html_error(
        expected_title="400 Bad Request",
        expected_message="Invalid parameters"
    )
    print("\nТест пройден: ошибка для массива получена")


@allure.title("Неавторизованный доступ")
def test_unauthorized_access(mem_client):
    # Удаляем заголовок авторизации
    mem_client.headers.pop('Authorization', None)
    mem_client.get_all_memes()
    mem_client.check_status(401)
    print("\nТест пройден: неавторизованный доступ отклонен")


@allure.title("Успешная авторизация")
def test_successful_authorization(auth_client):
    auth_client.authorize(name="TestUser")
    auth_client.check_status(200)
    assert hasattr(auth_client, 'token'), "Токен не получен"
    assert auth_client.token, "Токен пустой"
    print(f"\nТокен получен: {auth_client.token}")


@allure.title("GET /meme - Получение мемов с авторизацией 200")
def test_get_memes_with_auth(mem_client):
    mem_client.get_all_memes()
    mem_client.check_status(200)
    print("Ответ получен, статус 200")

    response = mem_client.check_json_response()
    assert isinstance(response, dict), "Ответ должен быть словарем"
    assert 'data' in response, "В ответе должно быть поле data"

# pytest test_api_final.py::test_get_memes_with_auth -v -s

@allure.title("Проверка валидности токена")
def test_token_validation(authorized_client):
    with allure.step("Проверка валидности токена авторизованного пользователя"):
        authorized_client.check_token()
        authorized_client.check_status(200)
        response_text = authorized_client.response.text
        print(f"Ответ сервера: {response_text}")

        assert authorized_client.response.text.startswith("Token is alive."), (
            f"Ответ сервера должен начинаться с 'Token is alive.',"
            f"получено: '{authorized_client.response.text}'"
        )
# pytest test_api_final.py -v -s
# pytest test_api_final.py::test_token_validation -v -s


@allure.title("GET /meme/{id} - Получение мема по ID - 200")
def test_get_single_meme(mem_client, existing_meme_id):
    with allure.step("Получение мема по ID"):
        mem_client.get_meme_by_id(existing_meme_id)
        mem_client.check_status(200)

    with allure.step("Проверка данных мема"):
        meme_data = mem_client.check_json_response()
        print(f"Ответ сервера:{meme_data}")

        assert meme_data['id'] == existing_meme_id, (
            f"ID полученного мема ({meme_data['id']}) "
            f"не совпадает с запрошенным ({existing_meme_id})"
        )

# pytest test_api_final.py::test_get_single_meme -v -s

@allure.title("GET /meme/{id} - Неавторизованный доступ к мему по ID - 401")
def test_get_single_meme_unauthorized(mem_client, unauthorized_mem_client):
    with allure.step("Получаем ID существующего мема через авторизованный клиент"):
        mem_client.get_all_memes()
        mem_client.check_status(200)
        test_id = mem_client.check_json_response()['data'][0]['id']
        print(f"Получен ID мема для теста: {test_id}")

    with allure.step("Проверяем доступ без авторизации"):
        unauthorized_mem_client.get_meme_by_id(test_id)
        unauthorized_mem_client.check_status(401)
        print("Получен ожидаемый статус 401 Unauthorized")

    with allure.step("Проверяем содержимое ошибки"):
        response_text = unauthorized_mem_client.response.text
        print(f"Ответ сервера: {response_text}")

        assert "<title>401 Unauthorized</title>" in response_text, "Неверный HTML-заголовок ошибки"
        assert "<h1>Unauthorized</h1>" in response_text, "Неверный заголовок страницы"
        assert "Not authorized" in response_text, "Неверное сообщение об ошибке"

# pytest test_api_final.py::test_get_single_meme_unauthorized -v -s

@allure.title("GET /meme/{id} - Запрос несуществующего мема - 404")
def test_get_nonexistent_meme(mem_client, nonexistent_meme_id):
    with allure.step("Отправка запроса несуществующего мема"):
        print(f"Используем тестовый ID: {nonexistent_meme_id}")
        mem_client.get_meme_by_id(nonexistent_meme_id)
        mem_client.check_status(404)

        response_text = mem_client.response.text
        allure.attach(
            f"Запрошенный ID: {nonexistent_meme_id}\n"
            f"Ответ сервера:\n{response_text}",
            name="Детали ответа"
        )
        print(f"Получен ожидаемый статус 404:\n{response_text}")

        assert "<title>404 Not Found</title>" in response_text, "Неверный заголовок ошибки"
        assert "<h1>Not Found</h1>" in response_text, "Неверный заголовок страницы"
        assert "The requested URL was not found" in response_text, "Неверное сообщение об ошибке"

# pytest test_api_final.py::test_get_nonexistent_meme -v -s

@allure.title("POST /meme - Успешное создание мема - 200")
def test_create_meme_success(post_client, delete_client):
    with allure.step("Подготовка тестовых данных"):
        test_data = {
            "text": "Funny Python Meme",
            "url": "https://example.com/python_meme.jpg",
            "tags": ["python", "testing"],
            "info": {"author": "pytest"}
        }

    with allure.step("Отправка запроса и проверка ответа"):
        post_client.create_meme(**test_data)
        post_client.check_status(200)
        response = post_client.check_json_response()  # Проверяем что ответ JSON

        # Проверка полей через check_json_field()
        post_client.check_json_field('id')
        post_client.check_json_field('text', test_data['text'])
        post_client.check_json_field('url', test_data['url'])
        post_client.check_json_field('info', test_data['info'])
        post_client.check_json_field('updated_by')

        # Проверка тегов
        post_client.check_tags(test_data['tags'])

        meme_id = response['id']
        print(f"Создан мем с ID: {meme_id}")

    with allure.step("Удаление созданного мема"):
        delete_client.delete_meme(meme_id)
        delete_client.check_status(200)
        print(f"Мем {meme_id} успешно удален")

# pytest test_api_final.py::test_create_meme_success -v -s

@allure.title("POST /meme - Попытка создать мем без авторизации 401 Unauthorized")
def test_create_meme_unauthorized(unauthorized_post_client):
    with allure.step("Подготовка тестовых данных"):
        test_data = {
            "text": "Funny Python Meme",
            "url": "https://example.com/python_meme.jpg",
            "tags": ["python", "testing"],
            "info": {"author": "pytest"}
        }

    with allure.step("Попытка создать мем без авторизации"):
        response = unauthorized_post_client.create_meme(**test_data)

    with allure.step("Проверка ошибки 401 Unauthorized"):
        unauthorized_post_client.check_html_error(
            expected_title="401 Unauthorized",
            expected_message="Not authorized"
        )
        print(f"Ответ сервера: {response.text}")

# pytest test_api_final.py::test_create_meme_unauthorized -v -s


@allure.title("POST /meme - Проверка обязательности полей - 400")
@pytest.mark.parametrize("missing_field", ["text", "url", "tags", "info"])
def test_create_meme_missing_field(post_client, missing_field):
    with allure.step("Подготовка тестовых данных"):
        test_data = {
            "text": "Funny Python Meme",
            "url": "https://example.com/python_meme.jpg",
            "tags": ["python", "testing"],
            "info": {"author": "pytest"}
       }

    original_value = test_data.pop(missing_field)
    print(f"Удалено поле {missing_field}, значение было: {original_value}")
    print(f"Данные для отправки: {test_data}")

    with allure.step(f"Создание мема без поля '{missing_field}' и получение 400"):
        post_client.create_fail_meme(meme_data=test_data)  # Передаем словарь

    with allure.step("Проверка ответа сервера"):
        print("Проверяем ответ...")
        post_client.check_status(400)
        print("Получен ожидаемый статус 400")

    debug_info = (
        f"\n=== Debug Info ===\n"
        f"Отсутствующее поле: {missing_field}\n"
        f"Отправленные данные: {test_data}\n"
        f"Ответ сервера:\n{post_client.response.text}\n"
        f"Status Code: {post_client.response.status_code}\n"
        f"=================="
    )

    allure.attach(
        f"Missing field: {missing_field}\n"
        f"Request data: {test_data}\n"
        f"Response: {post_client.response.text}",
        name="Debug info"
    )

    print(debug_info)

# pytest test_api_final.py::test_create_meme_missing_field -v -s


@allure.title("PUT /meme/<id> - Обновление мема без авторизации - 401")
def test_update_meme_unauthorized(create_meme_for_update, unauthorized_put_client):
    meme_id = create_meme_for_update
    print(f"\n[DEBUG] Создан тестовый мем с ID: {meme_id}")

    with allure.step("Попытка обновления без токена и получение 401"):
        unauthorized_put_client.update_meme(
            meme_id=1,
            text="Unauthorized try",
            url="https://example.com/fake.jpg",
            tags=["test"],
            info={"error": "expected"}
        )
        unauthorized_put_client.check_status(401)
        print(unauthorized_put_client.response.text)


@allure.title("PUT /meme/<id> - Обновление мема")
def test_update_meme(post_client, put_client):
    with allure.step("Создание тестового мема"):
        post_client.create_meme(
            text="Original Python Meme",
            url="https://example.com/original.jpg",
            tags=["python", "original"],
            info={"author": "pytest"}
        )

        post_client.check_status(200)
        meme_id = post_client.response.json()["id"]
        print(f"Создан мем с ID, {meme_id}")

    with allure.step("Обновление данных мема"):
        updated_text = "Updated Python Meme"
        updated_url = "https://example.com/updated.jpg"
        updated_tags = ["python", "updated"]
        updated_info = {"author": "pytest-updated"}

        response = put_client.update_meme(
            meme_id=meme_id,
            text=updated_text,
            url=updated_url,
            tags=updated_tags,
            info=updated_info
        )

        print("Статус:", response.status_code)
        print("Ответ:", response.text)
        put_client.check_status(200)
        print("Мем успешно обновлён!")

    with allure.step("Проверка обновленных данных мема"):
        put_client.check_updated_data(
            expected_url=updated_url,
            expected_text=updated_text,
            expected_info=updated_info,
            expected_tags=updated_tags
        )


@allure.title("Успешное удаление мема")
def test_successful_delete(create_meme_for_update, delete_client):
    meme_id = create_meme_for_update
    print(f"\n[DEBUG] Создан тестовый мем с ID: {meme_id}")

    with allure.step("Удаление тестового мема"):
        delete_client.delete_meme(meme_id)
        delete_client.check_successful_delete(meme_id)
        print(f"Мем с ID: {meme_id} успешно удалён")

        allure.attach(
            f"Удалён мем ID: {meme_id}\n"
            f"Ответ сервера: {delete_client.response.text}",
            name="Результат удаления"
        )

# pytest test_api_final.py::test_successful_delete -v -s


@allure.title("Проверка удаления несуществующего мема")
def test_repeated_delete(delete_client):
    with allure.step("Попытка удалить заведомо несуществующий мем"):
        non_meme_id = 999999
        delete_client.delete_meme(non_meme_id)
        delete_client.check_repeated_delete(non_meme_id)

        allure.attach(
            f"Запрошено удаление ID: {non_meme_id}\n"
            f"Статус: {delete_client.response.status_code}\n"
            f"Ответ: {delete_client.response.text}",
            name="Результат удаления",
            attachment_type=allure.attachment_type.TEXT
        )
    print(f"Проверено удаление несуществующего мема ID: {non_meme_id}")
    print(f"Тело ответа: {delete_client.response.text}")


@allure.title("Попытка удаления чужого мема")
def test_unauthorization_delete(create_meme_for_update, other_user_delete_client, delete_client, post_client):
    meme_id = create_meme_for_update
    print(f"\n[DEBUG] Создан тестовый мем с ID: {meme_id}")

    with allure.step("Попытка удаления чужого мема другим пользователем"):
        other_user_delete_client.delete_meme(meme_id)
        other_user_delete_client.check_unauthorized_delete()
        print(f"Проверено: OTHER-user не смог удалить мем: {meme_id}")

    with allure.step("Проверка удаления владельцем"):
        # Синхронизируем токен владельца
        delete_client.headers['Authorization'] = post_client.headers['Authorization']
        delete_client.delete_meme(meme_id)
        delete_client.check_successful_delete(meme_id)

        allure.attach(
            f"Мем ID: {meme_id}\n"
            f"Статус удаления: {delete_client.response.status_code}\n"
            f"Ответ сервера: {delete_client.response.text}",
            name="Результат удаления владельцем"
        )

        print(
            f" Мем: {meme_id} Доступен владельцу \n"
            f"Статус ответа на удаление: {delete_client.response.status_code}\n"
            f"Тело ответа: {delete_client.response.text}"
        )

# rm -rf allure-results
# pytest --alluredir=allure-results
# allure serve allure-results
