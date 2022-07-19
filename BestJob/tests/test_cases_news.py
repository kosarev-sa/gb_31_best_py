import pytest
import allure
from resources import TestData
from news.models import News
from django.urls import reverse


class TestNews:
    path_create = reverse('news:create_news')

    @allure.suite('News')
    @pytest.mark.all
    @pytest.mark.positive
    @pytest.mark.django_db
    @pytest.mark.parametrize('news', TestData.NEWS_POSITIVE, indirect=True)
    @allure.title('Создание новости')
    def test_positive_create_news(self, moderator_client, news, image):
        with allure.step('Создаем новость'):
            news['image'] = image
            response = moderator_client.post(self.path_create, data=news)
            assert response.status_code == 302, 'Новость не была создана'
            news['obj'] = News.objects.latest('id')

    @allure.suite('News')
    @pytest.mark.all
    @pytest.mark.negative
    @pytest.mark.django_db
    @pytest.mark.parametrize('news', TestData.NEWS_INSUFFICIENT, indirect=True)
    @allure.title('Создание новости без обязательных полей')
    def test_insufficient_create_news(self, moderator_client, news):
        with allure.step('Создаем новость'):
            response = moderator_client.post(self.path_create,  data=news)
            assert 'Обязательное поле.' in response.content.decode(), 'Новость была создана'

    @allure.suite('News')
    @pytest.mark.all
    @pytest.mark.negative
    @pytest.mark.django_db
    @pytest.mark.parametrize('news', TestData.NEWS_INVALID_FIELDS, indirect=True)
    @allure.title('Создание новости с невалидными значениями полей')
    def test_invalid_create_news(self, moderator_client, news):
        with allure.step('Создаем новость'):
            response = moderator_client.post(self.path_create,  data=news)
            assert 'Убедитесь, что это значение содержит не более 500 символов' in response.content.decode(), \
                'Новость была создана'

    @allure.suite('News')
    @pytest.mark.all
    @pytest.mark.positive
    @pytest.mark.urls
    @pytest.mark.parametrize('url', TestData.NEWS_URLS)
    @allure.title('Проверяем доступность адресов')
    def test_positive_availability(self, moderator_client, url):
        response = moderator_client.get(url)
        assert response.status_code == 200, 'Ресурс недоступен'
