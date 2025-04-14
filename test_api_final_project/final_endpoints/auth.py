import allure
import requests
from .final_endpoint import FinalEndpoint


class Auth(FinalEndpoint):
    @allure.step("Авторизация пользователя {name}")
    def authorize(self, name):
        """POST /authorize для получения токена"""
        self.response = requests.post(
            f"{self.base_url}/authorize",
            json={"name": name},
            headers=self.headers
        )
        self.token = self.response.json().get('token')
        if self.token:
            self.headers['Authorization'] = self.token
        return self.response

    @allure.step("Проверить валидность токена")
    def check_token(self, token=None):
        """GET /authorize/<token> для проверки токена"""
        check_token = token or self.token
        self.response = requests.get(
            f"{self.base_url}/authorize/{check_token}",
            headers=self.headers
        )
        return self.response

    @allure.step("Проверить авторизацию с невалидными данными")
    def authorize_invalid(self, json_data):
        """POST /authorize с некорректными данными"""
        self.response = requests.post(
            f"{self.base_url}/authorize",
            json=json_data,
            headers=self.headers
        )
        return self.response
