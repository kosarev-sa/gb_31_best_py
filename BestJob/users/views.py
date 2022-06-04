from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import UpdateView, FormView, ListView, DetailView

from BestJob.mixin import BaseClassContextMixin, UserDispatchMixin
from users.forms import WorkerProfileForm, EmployerProfileForm, ModeratorProfileForm, UserLoginForm, UserRegisterForm
from users.models import WorkerProfile, EmployerProfile, ModeratorProfile, User


class WorkerProfileView(UpdateView):
    """view для профиля соискателя"""
    model = WorkerProfile
    template_name = 'employee_profile.html'
    form_class = WorkerProfileForm

    # success_url = reverse_lazy()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerProfileView, self).get_context_data(**kwargs)
        return context


class EmployerProfileView(ListView, BaseClassContextMixin):
    """view для просмотра работодателей"""
    model = EmployerProfile
    template_name = 'employers.html'
    # paginate_by = 3
    title = 'BestJob | Работодатели'

    def get_context_data(self, **kwargs):
        context = super(EmployerProfileView, self).get_context_data(**kwargs)
        context.update({
            'employers': EmployerProfile.objects.all(),
        })
        return context

class EmployerDetailView(DetailView, BaseClassContextMixin):
    """view для просмотра выбранного работодателя"""
    model = EmployerProfile
    template_name = 'employers_detail.html'
    title = 'BestJob | Работодатель'


class EmployerProfileFormView(UpdateView, BaseClassContextMixin, UserDispatchMixin):
    """view для профиля работодателя"""
    model = EmployerProfile
    form_class = EmployerProfileForm
    template_name = 'employer_profile.html'
    success_url = reverse_lazy('users:employer_profile')
    title = 'BestJob | Профайл работодателя'

    # def get_object(self, queryset=None):
    #     return get_object_or_404(User, pk=self.request.employer_profile.pk)


class ModeratorProfileView(UpdateView):
    """view для профиля модератора"""

    model = ModeratorProfile
    template_name = 'moderator_profile.html'
    form_class = ModeratorProfileForm
    success_url = reverse_lazy('users:moderator_profile')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ModeratorProfileView, self).get_context_data(**kwargs)
        return context


class UserLoginView(LoginView):
    """view для логина"""
    template_name = 'user_login.html'
    from_class = UserLoginForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(UserLoginView, self).get_context_data()
        return context


class UserRegisterView(FormView):
    """view для регистрации"""
    model = User
    template_name = 'user_register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super(UserRegisterView, self).get_context_data()
        return context


class UserLogoutView(LogoutView):
    """view для выхода из-под учетки"""
    template_name = 'news.html'
