from haystack import indexes

from cvs.models import CV

class CVIndex(indexes.SearchIndex, indexes.Indexable):
    """класс для индексирования всех резюме"""
    text = indexes.CharField(document=True, use_template=True, template_name="search/cv_text.txt")
    name = indexes.CharField(model_attr='post')
    salary = indexes.IntegerField(model_attr='salary', null=True)
    speciality = indexes.CharField(model_attr='speciality')
    education_level = indexes.IntegerField(model_attr='education_level')
    moving = indexes.IntegerField(model_attr='moving')
    status_id = indexes.IntegerField(model_attr='status_id')


    def get_model(self):
        return CV

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
