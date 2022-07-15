import pytest
import allure
from resources import TestData
from vacancies.models import Vacancy
from django.urls import reverse


class TestVacancy:
    path_create = reverse('vacancy:create_vacancy')

    @allure.suite('Vacancy')
    @pytest.mark.all
    @pytest.mark.positive
    @pytest.mark.django_db
    @pytest.mark.parametrize('vacancy', TestData.VACANCY_POSITIVE, indirect=True)
    @allure.title('Создание вакансии')
    def test_positive_create_vacancy(self, employer_client, vacancy):
        with allure.step('Создаем вакансию'):
            response = employer_client.post(self.path_create, data=vacancy)
            assert response.status_code in [200, 302], 'Вакансия не была создана'
            vacancy['obj'] = Vacancy.objects.latest('id')

    @allure.suite('Vacancy')
    @pytest.mark.all
    @pytest.mark.negative
    @pytest.mark.django_db
    @pytest.mark.parametrize('vacancy', TestData.VACANCY_INSUFFICIENT, indirect=True)
    @allure.title('Создание вакансии без обязательных полей')
    def test_insufficient_create_vacancy(self, employer_client, vacancy):
        with allure.step('Создаем новость'):
            response = employer_client.post(self.path_create, data=vacancy)
            assert 'Обязательное поле.' in response.content.decode(), 'Вакансия была создана'

    @allure.suite('Vacancy')
    @pytest.mark.all
    @pytest.mark.negative
    @pytest.mark.django_db
    @pytest.mark.parametrize('vacancy', TestData.VACANCY_INVALID_FIELDS, indirect=True)
    @allure.title('Создание вакансии с невалидными значениями полей')
    def test_invalid_create_vacancy(self, employer_client, vacancy):
        with allure.step('Создаем новость'):
            response = employer_client.post(self.path_create, data=vacancy)
            assert ('Убедитесь, что вы ввели не более' in response.content.decode()
                    or 'Название должно быть не более 50 символов.' in response.content.decode()
                    or 'Убедитесь, что это значение содержит' in response.content.decode()), 'Вакансия была создана'

    @allure.suite('Vacancy')
    @pytest.mark.all
    @pytest.mark.positive
    @pytest.mark.urls
    @pytest.mark.parametrize('url', TestData.VACANCY_URLS)
    @allure.title('Проверяем доступность адресов')
    def test_positive_availability(self, employer_client, url):
        response = employer_client.get(url)
        assert response.status_code == 200, 'Ресурс недоступен'
