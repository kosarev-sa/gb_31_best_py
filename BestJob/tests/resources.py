from random import randint, choice
from data_generator import DataGenerator
from vacancies.models import EXPERIENCE
from search.models import Currency

dg = DataGenerator


class TestData:
    NEWS_POSITIVE = [
        {
            'title': dg.faker.text(50),
            'body': dg.faker.text(500),
            'image': 'replace'
        },
        {
            'title': '!' * 500,
            'body': dg.faker.text(500),
            'is_active': False,
            'image': 'replace'

        },
    ]

    NEWS_INSUFFICIENT = [
        {
        },
        {
            'body': dg.faker.text(500),
            'image': 'replace',
            'is_active': False,

        },
        {
            'title': dg.faker.text(500),
            'image': 'replace',
            'is_active': True,

        },
        {
            'body': dg.faker.text(500),
            'title': dg.faker.text(500),
        },
    ]

    NEWS_INVALID_FIELDS = [
        {
            'title': '1' * 501,
            'body': dg.faker.text(500),
            'image': 'replace'
        }
    ]

    VACANCY_POSITIVE = [
        {
            'status': 'replace',
            'specialization': 'replace',
            'is_active': True,
            'name': dg.faker.text(50),
            'experience': choice(EXPERIENCE)[0],
            'city': 'Москва',
            'description': dg.faker.text(500),
            'salary_from': randint(10000, 100000),
            'salary_to': randint(100000, 200000),
            'currency': Currency.RUB,
            'salary_on_hand': True,
            'moderators_comment': dg.faker.text(500)
        },
        {
            'name': dg.faker.text(10),
            'status': 'replace',
            'specialization': 'replace',
            'is_active': True,
            'currency': Currency.EUR,
        },
        {
            'status': 'replace',
            'specialization': 'replace',
            'is_active': True,
            'name': dg.faker.text(50),
            'experience': choice(EXPERIENCE)[0],
            'city': '1' * 20,
            'description': dg.faker.text(500),
            'salary_from': 1111111.1,
            'salary_to': 1111111.2,
            'currency': Currency.EUR,
            'salary_on_hand': True,
            'moderators_comment': dg.faker.text(500)
        },
    ]

    VACANCY_INSUFFICIENT = [
        {
        },
        {
            'status': 'replace',
            'is_active': True,
            'name': dg.faker.text(50),
            'experience': choice(EXPERIENCE)[0],
            'city': 'Москва',
            'description': dg.faker.text(500),
            'salary_from': randint(10000, 100000),
            'salary_to': randint(100000, 200000),
            'currency': Currency.RUB,
            'salary_on_hand': True,
            'moderators_comment': dg.faker.text(500)
        },
        {
            'status': 'replace',
            'specialization': 'replace',
            'is_active': True,
            'name': dg.faker.text(50),
            'experience': choice(EXPERIENCE)[0],
            'city': 'Москва',
            'description': dg.faker.text(500),
            'salary_from': randint(10000, 100000),
            'salary_to': randint(100000, 200000),
            'salary_on_hand': True,
            'moderators_comment': dg.faker.text(500)
        },
    ]

    VACANCY_INVALID_FIELDS = [
        {
            'status': 'replace',
            'specialization': 'replace',
            'is_active': True,
            'name': '1' * 257,
            'experience': choice(EXPERIENCE)[0],
            'city': 'Москва',
            'description': dg.faker.text(500),
            'salary_from': randint(10000, 100000),
            'salary_to': randint(100000, 200000),
            'currency': Currency.RUB,
            'salary_on_hand': True,
            'moderators_comment': dg.faker.text(500)
        },
        {
            'status': 'replace',
            'specialization': 'replace',
            'is_active': True,
            'name': dg.faker.text(50),
            'experience': choice(EXPERIENCE)[0],
            'city': '1' * 21,
            'description': dg.faker.text(500),
            'salary_from': randint(10000, 100000),
            'salary_to': randint(100000, 200000),
            'currency': Currency.RUB,
            'salary_on_hand': True,
            'moderators_comment': dg.faker.text(500)
        },
        {
            'status': 'replace',
            'specialization': 'replace',
            'is_active': True,
            'name': dg.faker.text(50),
            'experience': choice(EXPERIENCE)[0],
            'city': 'Москва',
            'description': dg.faker.text(500),
            'salary_from': 11111111.1,
            'salary_to': randint(100000, 200000),
            'currency': Currency.RUB,
            'salary_on_hand': True,
            'moderators_comment': dg.faker.text(500)
        },
        {
            'status': 'replace',
            'specialization': 'replace',
            'is_active': True,
            'name': dg.faker.text(50),
            'experience': choice(EXPERIENCE)[0],
            'city': 'Москва',
            'description': dg.faker.text(500),
            'salary_from': randint(10000, 100000),
            'salary_to': 11111211.1,
            'currency': Currency.RUB,
            'salary_on_hand': True,
            'moderators_comment': dg.faker.text(500)
        },
    ]

    NEWS_URLS = [
        '/news/all/',
        '/news/list/',
        '/news/create/',
    ]

    VACANCY_URLS = [
        '/vacancies/all/',
        '/vacancies/create/',
        '/vacancies/update/1/',
        '/vacancies/recommended/2/',
        '/vacancies/moderator_vacancy/',
        '/vacancies/moderator_vacancy_approve/2/',
        '/vacancies/detail/2/',
    ]

    CVS_URLS = [
        '/cvs/all/',
        '/cvs/create/',
        '/cvs/update/1/',
        '/cvs/detail/2/',
        '/cvs/create_education/1/',
        '/cvs/create_language/1/',
        '/cvs/moderator_cvs_approve/1/',
        '/cvs/cv_recommended/1/',
        '/cvs/moderator_cvs/',
    ]
