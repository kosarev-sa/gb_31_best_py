from haystack import indexes

from vacancies.models import Vacancy


class VacancyIndex(indexes.SearchIndex, indexes.Indexable):
    """класс для индексирования всех вакансий"""
    text = indexes.CharField(document=True, use_template=True, template_name="search/vacancy_text.txt")
    name = indexes.CharField(model_attr='name')
    specialization = indexes.CharField(model_attr='specialization')
    experience = indexes.CharField(model_attr='experience')
    description = indexes.CharField(model_attr='description')
    salary_from = indexes.IntegerField(model_attr='salary_from', null=True)
    salary_to = indexes.IntegerField(model_attr='salary_to', null=True)
    salary_on_hand = indexes.BooleanField(model_attr='salary_on_hand')
    status_id = indexes.IntegerField(model_attr='status_id')



    def get_model(self):
        return Vacancy

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
