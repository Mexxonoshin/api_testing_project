import allure
import requests
from .final_endpoint import FinalEndpoint


class DeleteMem(FinalEndpoint):
    def delete_meme(self, meme_id: int):
        self.response = requests.delete(
            f"{self.base_url}/meme/{meme_id}",
            headers=self.headers
        )
        return self.response

    @allure.step("Проверка успешного удаления")
    def check_successful_delete(self, meme_id: int):
        self.check_status(200)

        response_text = self.response.text.strip()

        expected_response = f"Meme with id {meme_id} successfully deleted"
        assert response_text == expected_response, (
            f"Неверный ответ сервера.\n"
            f"Ожидалось: '{expected_response}'\n"
            f"Получено:  '{response_text}'"
        )
        check_response = requests.get(
            f"{self.base_url}/meme/{meme_id}",
            headers=self.headers
        )
        assert check_response.status_code == 404, "Мем все еще доступен"

    @allure.step("Проверка повторного удаления = несуществующего мема")
    def check_repeated_delete(self, meme_id: int):
        self.check_html_error(
            expected_title="404 Not Found",
            expected_message="Not Found",
            allowed_statuses=(404,)
        )

    @allure.step("Проверка удаления с неверным токеном")
    def check_unauthorized_delete(self):
        self.check_html_error(
            expected_title="403 Forbidden",
            expected_message="You are not the meme owner",
            allowed_statuses=(403,)
        )
