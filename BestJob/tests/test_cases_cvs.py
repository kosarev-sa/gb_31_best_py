import pytest
import allure
from resources import TestData


class TestCvs:

    @allure.suite('CVs')
    @pytest.mark.all
    @pytest.mark.positive
    @pytest.mark.urls
    @pytest.mark.parametrize('url', TestData.CVS_URLS)
    @allure.title('Проверяем доступность адресов')
    def test_positive_availability(self, worker_client, url):
        response = worker_client.get(url)
        assert response.status_code == 200, 'Ресурс недоступен'
