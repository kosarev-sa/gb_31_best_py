from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DeleteView

from search.models import Category, Employments, WorkSchedules, Languages, \
    LanguageLevels
from vacancies.forms import VacancyCreateForm, VacancyUpdateForm, VacancyDistributeForm
from vacancies.models import Vacancy
from users.models import EmployerProfile
from approvals.models import ApprovalStatus

class VacancyList(TemplateView):
    """view просмотра активных вакансий"""
    template_name = 'vacancy_list.html'
    list_of_vacancies = Vacancy.objects.all()

    def get(self, request, *args, **kwargs):
        super(VacancyList, self).get(request, *args, **kwargs)
        user_id = request.user.pk
        employer_id = EmployerProfile.objects.get(user=user_id)
        context = {
            'vacancies': Vacancy.objects.filter(employer_profile=employer_id, is_active=True),
            'employer': employer_id,
            'status': ApprovalStatus.objects.get(status='CHG')
        }
        return self.render_to_response(context)


class VacancyCreate(CreateView):
    """view создания вакансий"""
    model = Vacancy
    template_name = 'vacancy_create.html'
    form_class = VacancyCreateForm
    success_url = reverse_lazy('vacancy:vacancy_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacancyCreate, self).get_context_data(**kwargs)
        context['title'] = 'Новая вакансия'
        return context

    def get(self, request, *args, **kwargs):
        super(VacancyCreate, self).get(request, *args, **kwargs)
        employer = EmployerProfile.objects.get(user=request.user.pk)
        context = self.get_context_data()
        context['employer'] = employer
        context['employments'] = Employments.objects.all()
        context['schedules'] = WorkSchedules.objects.all()
        context['languages'] = Languages.objects.all()
        context['levels'] = LanguageLevels.objects.all()
        return self.render_to_response(context)









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
