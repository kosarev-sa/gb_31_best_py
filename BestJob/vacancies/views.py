from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

from vacancies.forms import VacancyCreateForm, VacancyUpdateForm, VacancyDistributeForm
from vacancies.models import Vacancy


class VacancyList(ListView):
    """view просмотра активных вакансий"""
    model = Vacancy
    template_name = 'vacancy_list.html'
    context_object_name = 'vacancies_list'
    queryset = Vacancy.objects.filter(is_active=True)


class VacancyCreate(CreateView):
    """view создания вакансий"""
    model = Vacancy
    template_name = 'vacancy_create.html'
    form_class = VacancyCreateForm
    success_url = reverse_lazy('vacancy:vacancy_list')


class VacancyUpdate(UpdateView):
    """view изменения вакансий"""
    model = Vacancy
    template_name = 'vacancy_update.html'
    form_class = VacancyUpdateForm
    success_url = reverse_lazy('vacancy:vacancy_list')


class VacancyDelete(DeleteView):
    """view удаления вакансий"""
    model = Vacancy
    template_name = 'vacancy_delete.html'
    success_url = reverse_lazy('vacancy:vacancy_list')


class VacancyDistribute(UpdateView):
    """view для размещения вакансий"""
    model = Vacancy
    template_name = 'vacancy_distribute.html'
    form_class = VacancyDistributeForm
    success_url = reverse_lazy('vacancy:vacancy_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacancyDistribute, self).get_context_data(**kwargs)
        return context
