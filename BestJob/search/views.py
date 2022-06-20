
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet

from cvs.models import CV
from search.form import CVSearchForm


class CVSearchView(SearchView):
    """My custom search view."""
    template_name = 'search/search_cv.html'
    queryset = SearchQuerySet().all()
    form_class = CVSearchForm
    model = CV

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     # further filter queryset based on some set of criteria
    #     return queryset.all()
    #
    # def get_context_data(self, *args, **kwargs):
    #     context = super(CVSerchView, self).get_context_data(*args, **kwargs)
    #     # do something
    #     return context



