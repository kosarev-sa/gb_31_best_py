from decimal import Decimal
from unicodedata import decimal

from django import forms
from haystack.forms import SearchForm

from approvals.management.commands.fill_db import load_from_json, JSON_PATH_SEARCH
from cvs.models import CV
from search.models import Category, Moving, EducationLevel
from vacancies.models import EXPERIENCE, Vacancy

categories = load_from_json(JSON_PATH_SEARCH + 'categories.json')
categories_list = [('-', '-----')] + [(category.get('code'), category.get('name')) for category in categories]


class CVSearchForm(SearchForm):
    """форма детального поиска резюме"""

    salary = forms.IntegerField(label='зарплата от', required=False)
    speciality = forms.ChoiceField(label='специальность',
                                   choices=categories_list,
                                   required=False)
    education_level = forms.ChoiceField(label='образование', choices=[('-', '-----')] + EducationLevel.choices,
                                        required=False)
    moving = forms.ChoiceField(label='возможность переезда', choices=[('-', '-----')] + Moving.choices,
                               required=False)

    def search(self):
        # Сначала берем весь список резюме
        sqs = super(CVSearchForm, self).search().models(CV)
        # должно быть либо опубликовано, либо одобренно
        sqs = sqs.filter(status_id__in=(2, 5))

        if not self.is_valid():
            return self.no_query_found()

        # если есть требование по зарплате - фильтруем
        if self.cleaned_data['salary']:
            sqs = sqs.filter(salary__gte=self.cleaned_data['salary'])

        # если есть требование по спеуиальности - фильтруем
        if self.cleaned_data['speciality'] != '-' and self.cleaned_data['speciality'] != '':
            sqs = sqs.filter(speciality=Category.objects.get(code=self.cleaned_data['speciality']))

        # если есть требование по образованию - фильтруем
        if self.cleaned_data['education_level'] != '-' and self.cleaned_data['education_level'] != '':
            sqs = sqs.filter(education_level=int(self.cleaned_data['education_level']))

        # если есть требование по переезду - фильтруем
        if self.cleaned_data['moving'] != '-' and self.cleaned_data['moving'] != '':
            sqs = sqs.filter(moving=int(self.cleaned_data['moving']))

        return sqs

    def __init__(self, *args, **kwargs):
        super(CVSearchForm, self).__init__(*args, **kwargs)
        self.fields['speciality'].widget.attrs.update({"class": "form-control"})
        self.fields['education_level'].widget.attrs.update(
            {"class": "form-control"})
        self.fields['moving'].widget.attrs.update({"class": "form-control"})
        self.fields['salary'].widget.attrs.update({"class": "form-control"})


class VacancySearchForm(SearchForm):
    """форма детального поиска вакансий"""
    salary_from = forms.IntegerField(label='зарплата от', required=False)
    salary_to = forms.IntegerField(label='зарплата до', required=False)
    # salary_on_hand = forms.CheckboxInput()

    salary_on_hand = forms.BooleanField(label='зарплата на руки', required=False)
    specialization = forms.ChoiceField(label='специальность',
                                       choices=categories_list,
                                       required=False)
    experience = forms.ChoiceField(label='опыт', choices=[('-', '-----')] + list(EXPERIENCE),
                                   required=False)

    def search(self):
        # Сначала берем весь список вакансий
        sqs = super(VacancySearchForm, self).search().models(Vacancy)
        # должно быть либо опубликовано, либо одобренно
        sqs = sqs.filter(status_id__in=(2, 5))

        if not self.is_valid():
            return self.no_query_found()

        # если есть требование по зарплате от - фильтруем
        if self.cleaned_data['salary_from']:
            sqs = sqs.filter(salary_to__gte=self.cleaned_data['salary_from'])

        # если есть требование по зарплате до - фильтруем
        if self.cleaned_data['salary_to']:
            sqs = sqs.filter(salary_from__lte=self.cleaned_data['salary_to'])

        # если есть требование по зарплате на руки - фильтруем
        if self.cleaned_data['salary_on_hand']:
            sqs = sqs.filter(salary_on_hand=self.cleaned_data['salary_on_hand'])

        # если есть требование по спеуиальности - фильтруем
        if self.cleaned_data['specialization'] != '-' and self.cleaned_data['specialization'] != '':
            sqs = sqs.filter(specialization=Category.objects.get(code=self.cleaned_data['specialization']))

        # если есть требование по опыту - фильтруем
        if self.cleaned_data['experience'] != '-' and self.cleaned_data['experience'] != '':
            sqs = sqs.filter(experience=self.cleaned_data['experience'])

        return sqs

    def __init__(self, *args, **kwargs):
        super(VacancySearchForm, self).__init__(*args, **kwargs)
        self.fields['specialization'].widget.attrs.update({"class": "form-control"})
        self.fields['experience'].widget.attrs.update(
            {"class": "form-control"})
        self.fields['salary_from'].widget.attrs.update({"class": "form-control"})
        self.fields['salary_to'].widget.attrs.update({"class": "form-control"})
        self.fields['salary_on_hand'].widget.attrs.update({"class": "form-check-input"})

