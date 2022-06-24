from django import forms
from haystack.forms import SearchForm

from cvs.models import CV
from search.models import Category, Moving, EducationLevel


class CVSearchForm(SearchForm):
    """форма детального поиска резюме"""
    salary = forms.DecimalField(label='зарплата от', required=False)
    speciality = forms.ChoiceField(label='специальность',
                                   choices=[('-', '-----')] + list(Category.objects.values_list('code', 'name')),
                                   required=False)
    education_level = forms.ChoiceField(label='образование', choices=[('-', '-----')] + EducationLevel.choices,
                                        required=False)
    moving = forms.ChoiceField(label='возможность переезда', choices=[('-', '-----')] + Moving.choices,
                               required=False)

    def search(self):
        # Сначала берем весь список резюме
        sqs = super(CVSearchForm, self).search().models(CV)

        sqs.filter()

        if not self.is_valid():
            return self.no_query_found()

        # если есть требование по зарплате - фильтруем
        if self.cleaned_data['salary']:
            sqs = sqs.filter(salary__gte=self.cleaned_data['salary'])

        # если есть требование по спеуиальности - фильтруем
        if self.cleaned_data['speciality'] != '-' and self.cleaned_data['speciality'] != '':
            sqs = sqs.filter(speciality=Category.objects.get(code=self.cleaned_data['speciality']))

        # если есть требование по образованию - фильтруем
        if self.cleaned_data['education_level'] != '-' and  self.cleaned_data['education_level'] != '':
            sqs = sqs.filter(education_level=int(self.cleaned_data['education_level']))

        # если есть требование по переезду - фильтруем
        if self.cleaned_data['moving'] != '-' and self.cleaned_data['moving'] != '':
            sqs = sqs.filter(moving=int(self.cleaned_data['moving']))

        return sqs
