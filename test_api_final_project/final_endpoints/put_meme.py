import allure
import requests
from .final_endpoint import FinalEndpoint


class PutMem(FinalEndpoint):
    def update_meme(self, meme_id: int, text: str, url: str, tags: list, info: dict):
        self.response = requests.put(
            f"{self.base_url}/meme/{meme_id}",
            json={
                "id": meme_id,  # Добавьте id в тело запроса!
                "text": text,
                "url": url,
                "tags": tags,
                "info": info
            },
            headers=self.headers
        )
        return self.response

# Проверка соответствия обновленных данных

    def check_updated_data(self, expected_text: str, expected_url: str,
                           expected_tags: list, expected_info: dict):
        response_data = self.response.json()
        assert response_data["text"] == expected_text, \
            f"Текст не обновился. Ожидалось: {expected_text}, Получено: {response_data['text']}"

        assert response_data["url"] == expected_url, \
            f"URL не обновился. Ожидалось: {expected_url}, Получено: {response_data['url']}"

        assert response_data["tags"] == expected_tags, \
            f"Тэги не обновились. Ожидалось: {expected_tags}, Получено: {response_data['tags']}"

        assert response_data["info"] == expected_info, \
            f"Info не обновилось. Ожидалось: {expected_info}, Получено: {response_data['info']}"

        # Логирование успешной проверки
        debug_info = (
            f"\n=== Данные успешно обновлены ===\n"
            f"Текст: {response_data['text']}\n"
            f"URL: {response_data['url']}\n"
            f"Теги: {response_data['tags']}\n"
            f"Info: {response_data['info']}\n"
        )
        print(debug_info)
        allure.attach(debug_info, name="Проверка обновления")
