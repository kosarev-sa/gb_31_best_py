from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from cvs.forms import CVCreateForm, CVUpdateForm, CVDeleteForm, CVDistributeForm
from cvs.models import CV
from vacancies.forms import VacancyCreateForm, VacancyUpdateForm, VacancyDeleteForm, VacancyDistributeForm
from vacancies.models import Vacancy


class VacancyList(TemplateView):
    """view главной страницы с новостями"""
    template_name = 'vacancy_list.html'
    list_of_news = Vacancy.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacancyList, self).get_context_data(**kwargs)
        context['vanacies'] = self.list_of_news
        return context


class VacancyCreate(CreateView):
    """view для создания новостей"""
    model = Vacancy
    template_name = 'vacancy_create.html'
    form_class = VacancyCreateForm
    success_url = reverse_lazy('vacancy:vacancy_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacancyCreate, self).get_context_data(**kwargs)
        return context


class VacancyUpdate(UpdateView):
    """view для обновления новостей"""
    model = CV
    template_name = 'vacancy_update.html'
    form_class = VacancyUpdateForm
    success_url = reverse_lazy('vacancy:vacancy_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacancyUpdate, self).get_context_data(**kwargs)
        return context


class VacancyDelete(DeleteView):
    """view для обновления новостей"""
    model = CV
    template_name = 'vacancy_delete.html'
    form_class = VacancyDeleteForm
    success_url = reverse_lazy('vacancy:vacancy_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacancyDelete, self).get_context_data(**kwargs)
        return context


class VacancyDistribute(UpdateView):
    """view для обновления новостей"""
    model = CV
    template_name = 'vacancy_distribute.html'
    form_class = VacancyDistributeForm
    success_url = reverse_lazy('vacancy:vacancy_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacancyDistribute, self).get_context_data(**kwargs)
        return context
