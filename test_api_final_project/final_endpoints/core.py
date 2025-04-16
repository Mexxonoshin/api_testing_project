from test_api_final_project.final_endpoints.final_endpoint import FinalEndpoint
import allure


class CoreAPI(FinalEndpoint):
    @allure.step("Проверка главной страницы API")
    def check_welcome_page(self):
        self.get()  # GET-запрос к корневому эндпоинту
        self.check_status(200)
        assert "Hi there!" in self.response.text, "Не найдено приветственное сообщение"
        assert "simple API" in self.response.text, "Не найдено упоминание API"

        return self.response
