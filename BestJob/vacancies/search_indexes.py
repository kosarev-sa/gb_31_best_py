from haystack import indexes

from vacancies.models import Vacancy


class VacancyIndex(indexes.SearchIndex, indexes.Indexable):
    """класс для индексирования всех вакансий"""
    text = indexes.CharField(document=True, use_template=True, template_name="search/vacancy_text.txt")
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Vacancy

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
