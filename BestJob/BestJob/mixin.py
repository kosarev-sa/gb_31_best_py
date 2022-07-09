from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.base import View, ContextMixin
from BestJob.settings import UserRole
from favorites.models import EmployerFavorites, WorkerFavorites
from users.models import EmployerProfile, WorkerProfile


class CustomDispatchMixin(View):

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CustomDispatchMixin, self).dispatch(request, *args, **kwargs)


class BaseClassContextMixin(ContextMixin):
    title = ''

    def get_context_data(self, **kwargs):
        context = super(BaseClassContextMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context


class UserDispatchMixin(View):

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDispatchMixin, self).dispatch(request, *args, **kwargs)


class FavouriteListMixin(ContextMixin):
    """
    mixin to add list of favourites resume/cv in a context
    """

    def get_favourite_list(self):
        if self.request.user.is_authenticated:
            if self.request.user.role_id == UserRole.EMPLOYER:
                profile_id = EmployerProfile.objects.get(user_id=self.request.user.id).id
                return EmployerFavorites.objects.filter(employer_profile_id=profile_id).values_list('cv_id', flat=True)
            elif self.request.user.role_id == UserRole.WORKER:
                profile_id = WorkerProfile.objects.get(user_id=self.request.user.id).id
                return WorkerFavorites.objects.filter(worker_profile_id=profile_id).values_list('vacancy_id', flat=True)
        else:
            return []

    def get_context_data(self, **kwargs):
        context = super(FavouriteListMixin, self).get_context_data(**kwargs)
        context['favourite_list'] = self.get_favourite_list()
        return context

