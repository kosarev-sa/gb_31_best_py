from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DeleteView

from search.models import Category, Employments, WorkSchedules, Languages, \
    LanguageLevels
from vacancies.forms import VacancyCreateForm, VacancyUpdateForm, VacancyDistributeForm, ModeratorVacancyUpdateForm
from vacancies.models import Vacancy, WorkingHours
from users.models import EmployerProfile
from approvals.models import ApprovalStatus
from cvs.models import ConnectVacancyCv


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
            'status': ApprovalStatus.objects.get(status='APV')
        }
        return self.render_to_response(context)


class ModeratorVacancyList(TemplateView):
    """view просмотра вакансий модератором"""
    template_name = 'moderator_vacancy_list.html'

    def get(self, request, *args, **kwargs):
        super(ModeratorVacancyList, self).get(request, *args, **kwargs)
        # user_id = request.user.pk
        # employer_id = EmployerProfile.objects.get(user=user_id)
        context = self.get_context_data()
        context['vacancies_list'] = Vacancy.objects.all()
        return self.render_to_response(context)


class ResponseVacancyList(TemplateView):
    """view список откликов на вакансию работодателя"""
    template_name = 'vacancy_response_list.html'

    def get(self, request, *args, **kwargs):
        super(ResponseVacancyList, self).get(request, *args, **kwargs)
        employer_id = EmployerProfile.objects.get(user=request.user.pk)
        vacancy_employer_ids = [vacancy.id for vacancy in Vacancy.objects.filter(employer_profile=employer_id,
                                                                                 is_active=True)]
        context = {
            'responses': ConnectVacancyCv.objects.filter(vacancy_id__in=vacancy_employer_ids),
        }
        return self.render_to_response(context)


class ModeratorVacancyUpdate(UpdateView):
    """view изменения вакансий"""
    model = Vacancy
    template_name = 'moderator_vacancy_approve.html'
    form_class = ModeratorVacancyUpdateForm
    success_url = reverse_lazy('vacancy:moderator_vacancy_list')

    def get(self, request, *args, **kwargs):
        super(ModeratorVacancyUpdate, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        vac_id = self.kwargs['pk']
        vac = Vacancy.objects.get(pk=vac_id)
        vac_user_id = vac.employer_profile.user_id
        employer = EmployerProfile.objects.filter(user_id=vac_user_id)
        if employer:
            context['employer'] = employer.first()

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        vac_id = self.kwargs['pk']
        if form.is_valid():
            Vacancy.objects.filter(pk=vac_id).update(status=form.instance.status)
        return redirect(self.success_url)


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

    def post(self, request, *args, **kwargs):
        employer = EmployerProfile.objects.get(user=request.user.pk)
        start_status = ApprovalStatus.objects.get(status='CHG')
        form = self.form_class(data=request.POST)
        if form.is_valid():
            # сохраняем новую вакансию
            vacancy = form.save(commit=False)
            vacancy.employer_profile = employer
            vacancy.status = start_status
            vacancy.save()

            return redirect(self.success_url)
        else:
            print(form.errors)
        return self.form_invalid(form)


class VacancyUpdate(UpdateView):
    """view изменения вакансий"""
    model = Vacancy
    template_name = 'vacancy_update.html'
    form_class = VacancyUpdateForm
    success_url = reverse_lazy('vacancy:vacancy_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacancyUpdate, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        super(VacancyUpdate, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        vacancy_id = kwargs.get('pk')
        vacancy = Vacancy.objects.get(id=vacancy_id)
        # Временное решение до реализации get view для вакансии
        try:
            employer = EmployerProfile.objects.get(user=request.user.pk)
            context['employer'] = employer
        except Exception:
            print(f'Employer {request.user.pk} not exists')
        context['employments'] = Employments.objects.all()
        vacancy_schedules = [vacancy_sch.schedule_id for vacancy_sch in WorkingHours.objects.filter(vacancy=vacancy)]
        context['vacancy_schedules'] = vacancy_schedules
        context['languages'] = Languages.objects.all()
        context['levels'] = LanguageLevels.objects.all()
        context['schedules'] = WorkSchedules.objects.all()
        return self.render_to_response(context)

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = self.form_class(request.POST, instance=self.object)
    #
    #     if form.is_valid():
    #         self.object.save()
    #
    #         return redirect(self.success_url)
    #     else:
    #         print(form.errors)
    #     return self.form_invalid(form)


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
