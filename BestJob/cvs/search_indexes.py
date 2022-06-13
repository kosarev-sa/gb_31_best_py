from haystack import indexes

from cvs.models import CV

class CVIndex(indexes.SearchIndex, indexes.Indexable):
    """класс для индексирования всех резюме"""
    text = indexes.CharField(document=True, use_template=True, template_name="search/cv_text.txt")
    name = indexes.CharField(model_attr='post')

    def get_model(self):
        return CV

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
