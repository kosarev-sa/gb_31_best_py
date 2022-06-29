from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet

from cvs.models import CV
from search.form import CVSearchForm, VacancySearchForm
from vacancies.models import Vacancy


class CVSearchView(SearchView):
    """My custom search view."""
    template_name = 'search/search_cv.html'
    queryset = SearchQuerySet().all()
    form_class = CVSearchForm
    model = CV

class VacancySearchView(SearchView):
    """My custom search view."""
    template_name = 'search/search_vacancy.html'
    queryset = SearchQuerySet().all()
    form_class = VacancySearchForm
    model = Vacancy




