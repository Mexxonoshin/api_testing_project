import allure
import requests
from .final_endpoint import FinalEndpoint


class PostMem(FinalEndpoint):
    @allure.step("Добавление нового мема")
    def create_meme(self, text: str, url: str, tags: list, info: dict):
        meme_data = {
            "text": text,
            "url": url,
            "tags": tags,
            "info": info
        }
        self.response = requests.post(
            f"{self.base_url}/meme",
            json=meme_data,
            headers=self.headers
        )
        return self.response

    def create_fail_meme(self, **meme_data):
        """
        POST /meme - создание нового мема с ожидаемой ошибкой
        Принимает параметры как именованные аргументы или словарь
        """
        self.response = requests.post(
            f"{self.base_url}/meme",
            json=meme_data,
            headers=self.headers
        )
        return self.response

    def check_tags(self, expected_tags):
        with allure.step(f"Проверка тегов (ожидается: {expected_tags})"):
            actual_tags = self.response.json().get('tags',[])
            assert set(actual_tags) == set(expected_tags), (
                f"Теги не совпадают. Ожидалось: {expected_tags}, получено: {actual_tags}"
            )
            allure.attach(
                f"Ожидаемые: {expected_tags}\nФактические: {actual_tags}",
                name="Сравнение тегов",
                attachment_type=allure.attachment_type.TEXT
            )
