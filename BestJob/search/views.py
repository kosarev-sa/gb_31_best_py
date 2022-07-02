from django.contrib import messages
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
    paginate_by = 2

    def get_context_data(self, *args, **kwargs):
        context = super(CVSearchView, self).get_context_data(**kwargs)
        if self.request.user.id is None or self.request.user.role.id == 3:
            context['message_of_denied'] = 'Просматривать резюме могут только авторизованные ' \
                                           'работодатели!'
        return context


class VacancySearchView(SearchView):
    """My custom search view."""
    template_name = 'search/search_vacancy.html'
    queryset = SearchQuerySet().all()
    form_class = VacancySearchForm
    model = Vacancy
    paginate_by = 2

    def get_context_data(self, *args, **kwargs):
        context = super(VacancySearchView, self).get_context_data(**kwargs)
        if self.request.user.id is None or self.request.user.role.id == 2:
            context['message_of_denied'] = 'Просматривать вакансии могут только авторизованные ' \
                                           'соискатели!'
        return context
