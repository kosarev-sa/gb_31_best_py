import os
import pytest
import allure
import django
from random import randint
from django.test.utils import setup_test_environment
from django.core.files.uploadedfile import SimpleUploadedFile
django.setup()
setup_test_environment()
from users.models import ModeratorProfile, EmployerProfile, WorkerProfile
from news.models import News
from approvals.models import ApprovalStatus
from search.models import Category
from BestJob.settings import MEDIA_ROOT
from django.test.client import Client


@pytest.fixture(scope='session')
def moderator_client() -> Client:
    client = Client()
    client.login(username='moderator_1', password='1')
    return client


@pytest.fixture(scope='session')
def employer_client() -> Client:
    client = Client()
    client.login(username='employer_2', password='2')
    return client


@pytest.fixture(scope='session')
def worker_client() -> Client:
    client = Client()
    client.login(username='worker_11', password='11')
    return client


@pytest.fixture
def news(request, image) -> dict:
    news = request.param
    if news.get('image') == 'replace':
        news['image'] = image
    yield news

    if news.get('obj'):
        with allure.step(f'Удаляем созданную новость #{news["obj"].id}'):
            news['obj'].delete()

        with allure.step('Удаляем тестовую фотографию'):
            os.remove(os.path.join(MEDIA_ROOT, 'news_images', str(news['image'])))


@pytest.fixture(scope='session')
def default_news() -> News:
    return News.objects.all().latest('id')


@pytest.fixture(scope='session')
def default_specialization() -> Category:
    return Category.objects.all().latest('id')


@pytest.fixture(scope='session')
def default_status() -> ApprovalStatus:
    return ApprovalStatus.objects.all().latest('id')


@pytest.fixture
def vacancy(request, default_specialization, default_status) -> dict:
    vacancy = request.param
    if vacancy.get('specialization') == 'replace':
        vacancy['specialization'] = default_specialization.id
    if vacancy.get('status') == 'replace':
        vacancy['status'] = default_status.id

    yield vacancy

    if vacancy.get('obj'):
        with allure.step('Удаляем созданную вакансию'):
            vacancy['obj'].delete()


@pytest.fixture(scope='session')
def default_moderator() -> dict:
    with allure.step('Получаем профиль модератора'):
        moderator_obj = ModeratorProfile.objects.all().first()

    return moderator_obj


@pytest.fixture
def image() -> SimpleUploadedFile:
    name = f'{randint(1, 5)}.jpg'
    with open(os.path.join(MEDIA_ROOT, 'news_images', name), 'rb') as f:
        image = SimpleUploadedFile(f'tmp_{name}',
                                   f.read(), content_type="image")
        return image
