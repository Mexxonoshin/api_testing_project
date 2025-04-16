import allure
import requests


class FinalEndpoint:
    def __init__(self):
        self.base_url = 'http://167.172.172.115:52355'
        self.headers = {'Content-Type': 'application/json'}
        self.response = None
        self.token = None

    @allure.step("Отправка GET-запроса к {path}")
    def get(self, path=""):
        self.response = requests.get(
            f"{self.base_url}{path}",
            headers=self.headers
        )
        return self.response

    @allure.step("Проверка статуса {expected_status}")
    def check_status(self, expected_status):
        assert self.response.status_code == expected_status, (
            f"Ожидался {expected_status}, получен {self.response.status_code}"
        )

    def check_html_error(self, expected_title=None, expected_message=None, allowed_statuses=(400, 401, 403, 404)):
        # Проверяем, что статус ответа соответствует ожидаемым кодам
        assert self.response.status_code in allowed_statuses, (
            f"Недопустимый статус ответа: {self.response.status_code}. "
            f"Ожидалось один из: {allowed_statuses}."
        )
        response_text = self.response.text

        # Базовые проверки HTML-структуры
        assert "<title>" in response_text, "Отсутствует HTML-заголовок"
        assert "<h1>" in response_text, "Отсутствует заголовок ошибки"
        assert "<p>" in response_text, "Отсутствует текст сообщения"

        # Проверка заголовка (если указан)
        if expected_title:
            assert expected_title in response_text, (
                f"Заголовок страницы не содержит '{expected_title}'\n"
                f"Полный ответ:\n{response_text}"
            )

        # Проверка сообщения (если указано)
        if expected_message:
            assert expected_message in response_text, (
                f"Сообщение об ошибке не содержит '{expected_message}'\n"
                f"Полный ответ:\n{response_text}"
            )

    def check_token_exists(self):
        assert hasattr(self, 'token') and self.token, "Токен не получен"
        return self

    def check_json_response(self):
        assert 'application/json' in self.response.headers['Content-Type'], "Ответ не в JSON"
        return self.response.json()

    def check_json_field(self, field, expected_value=None):
        json_data = self.check_json_response()
        assert field in json_data, f"Нет поля '{field}' в ответе"
        if expected_value is not None:
            assert json_data[field] == expected_value, f"Поле '{field}' не равно '{expected_value}'"
        return self
