import allure
import requests
from .final_endpoint import FinalEndpoint


class GetMem(FinalEndpoint):
    @allure.step("Получить все мемы")
    def get_all_memes(self):
        """GET /meme - список всех мемов"""
        return self.get("/meme")

    @allure.step("Получить мем по ID")
    def get_meme_by_id(self, meme_id):
        """GET /meme/{id} - конкретный мем"""
        return self.get(f"/meme/{meme_id}")
