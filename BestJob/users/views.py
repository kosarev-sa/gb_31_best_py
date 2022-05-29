from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import UpdateView, FormView

from users.forms import EmployeeProfileForm, EmployerProfileForm, ModeratorProfileForm, UserLoginForm, UserRegisterForm
from users.models import WorkerProfile, EmployerProfile, ModeratorProfile, User


class EmployeeProfileView(UpdateView):
    """view для профиля соискателя"""
    model = WorkerProfile
    template_name = 'employee_profile.html'
    form_class = EmployeeProfileForm

    # success_url = reverse_lazy()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EmployeeProfileView, self).get_context_data(**kwargs)
        return context


class EmployerProfileView(UpdateView):
    """view для профиля работодателя"""

    model = EmployerProfile
    template_name = 'employer_profile.html'
    form_class = EmployerProfileForm
    success_url = reverse_lazy('users:employer_profile')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EmployerProfileView, self).get_context_data(**kwargs)
        return context


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
