from django.contrib import messages
from haystack.generic_views import SearchView
from haystack.views import SearchView as SearchViewStandard
from haystack.query import SearchQuerySet

from BestJob.mixin import FavouriteListMixin
from cvs.models import CV
from search.form import CVSearchForm, VacancySearchForm
from vacancies.models import Vacancy
from BestJob.settings import UserRole


class StandardSearch(SearchViewStandard, FavouriteListMixin):
    def extra_context(self):
        """
        Allows the addition of more context variables as needed.

        Must return a dictionary.
        """
        return {'favourite_list': self.get_favourite_list()}

class CVSearchView(SearchView, FavouriteListMixin):
    """My custom search view."""
    template_name = 'search/search_cv.html'
    queryset = SearchQuerySet().all()
    form_class = CVSearchForm
    model = CV
    paginate_by = 2

    def get_context_data(self, *args, **kwargs):
        context = super(CVSearchView, self).get_context_data(**kwargs)
        if self.request.user.id is None or self.request.user.role.id == UserRole.WORKER:
            context['message_of_denied'] = 'Просматривать резюме могут только авторизованные ' \
                                           'работодатели!'
        context['title'] = "Поиск резюме"
        context['heading'] = "Поиск резюме"
        return context


class VacancySearchView(SearchView, FavouriteListMixin):
    """My custom search view."""
    template_name = 'search/search_vacancy.html'
    queryset = SearchQuerySet().all()
    form_class = VacancySearchForm
    model = Vacancy
    paginate_by = 2

    def get_context_data(self, *args, **kwargs):
        context = super(VacancySearchView, self).get_context_data(**kwargs)
        if self.request.user.id is None or self.request.user.role.id == UserRole.EMPLOYER:
            context['message_of_denied'] = 'Просматривать вакансии могут только авторизованные ' \
                                           'соискатели!'
        context['title'] = "Поиск вакансий"
        context['heading'] = "Поиск вакансий"
        return context
