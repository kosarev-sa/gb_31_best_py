
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DeleteView, DetailView

from cvs.models import CV
from search.models import Category, Employments, WorkSchedules, Languages, \
    LanguageLevels
from vacancies.forms import VacancyCreateForm, VacancyUpdateForm, VacancyDistributeForm, ModeratorVacancyUpdateForm, \
    VacancyResponseForm
from vacancies.models import Vacancy
from users.models import EmployerProfile
from approvals.models import ApprovalStatus

from BestJob.mixin import BaseClassContextMixin, UserDispatchMixin
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

        context = self.get_context_data()
        context['title'] = 'Вакансии'
        context['vacancies_list'] = Vacancy.objects.exclude(status__status="NPB")

        return self.render_to_response(context)


class ResponseVacancyList(TemplateView):
    """view список откликов на вакансию работодателя"""
    template_name = 'vacancy_response_list.html'

    def get(self, request, *args, **kwargs):
        super(ResponseVacancyList, self).get(request, *args, **kwargs)
        employer_id = EmployerProfile.objects.get(user=request.user.pk)
        vacancies = Vacancy.objects.filter(employer_profile=employer_id, is_active=True)
        vacancies_cvs = []
        for vacancy in vacancies:
            vacancies_cvs.append((
                vacancy,
                ConnectVacancyCv.objects.filter(vacancy_id=vacancy.id),
            ))

        context = {
            'vacancies_cvs': vacancies_cvs,
        }
        return self.render_to_response(context)


class ResponseVacancyCVs(TemplateView):
    """view список резюме с откликом на вакансию"""
    template_name = 'vacancy_cvs.html'
    form_class = VacancyResponseForm

    def get(self, request, *args, **kwargs):
        super(ResponseVacancyCVs, self).get(request, *args, **kwargs)
        vacancy_id = kwargs['pk']
        context = {
            'form': self.form_class,
            'responses': ConnectVacancyCv.objects.filter(vacancy_id=vacancy_id),
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        vacancy_id = kwargs['pk']
        response_id = kwargs.get('resp_id')
        form = self.form_class(data=request.POST)
        if form.is_valid():
            ConnectVacancyCv.objects.filter(pk=response_id).update(status_employer=form.instance.status_employer)
            return redirect(reverse("vacancy:vacancy_cvs", args=(vacancy_id,)))


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
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        employer = EmployerProfile.objects.get(user=request.user.pk)
        start_status = ApprovalStatus.objects.get(status='NPB')
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
        # Временное решение до реализации get view для вакансии
        try:
            employer = EmployerProfile.objects.get(user=request.user.pk)
            context['employer'] = employer
        except Exception:
            print(f'Employer {request.user.pk} not exists')
        context['employments'] = Employments.objects.all()
        return self.render_to_response(context)


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


class VacancyOpenList(TemplateView, BaseClassContextMixin):
    """view просмотра активных вакансий любым пользователем"""
    template_name = 'vacancy_base.html'
    title = 'BestJob | Вакансии'

    def get(self, request, *args, **kwargs):
        super(VacancyOpenList, self).get(request, *args, **kwargs)
        context = {
            'vacancies': Vacancy.objects.filter(is_active=True),
        }
        return self.render_to_response(context)


class RecommendedVacancyList(ListView, BaseClassContextMixin):
    """view просмотра рекомендованных по резюме вакансий"""
    template_name = 'vacancy_list.html'
    model = Vacancy
    title = 'BestJob | Рекомендованные вакансии'

    def get(self, request, *args, **kwargs):
        super(RecommendedVacancyList, self).get(request, *args, **kwargs)
        cv = CV.objects.get(id=self.kwargs['pk'])
        context = {
            'vacancies': Vacancy.objects.filter(specialization=cv.speciality),
            'title': "Рекомендованные вакансии",
            'heading': "Рекомендованные вакансии",

            # Сделать переход в шапке, куда?
            # 'link': "",
            # 'heading_link': "",
        }

        return self.render_to_response(context)
        

class VacancyDetail(DetailView):
    """Просмотр одной вакансии независимо от регистрации"""
    model = Vacancy
    template_name = 'vacancy_detail.html'

    def get(self, request, *args, **kwargs):
        super(VacancyDetail, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        vacancy_id = kwargs.get('pk')
        vacancy = Vacancy.objects.get(id=vacancy_id)
        try:
            employer = EmployerProfile.objects.get(id=vacancy_id)
            context['vacancy'] = vacancy
            context['employer'] = employer
        except Exception:
            print(f'Employer not exists')
        context['employments'] = Employments.objects.all()

        return self.render_to_response(context)


def edit_vacancy_list(request, stat):
    """Обновление списка вакансий соглано статусу на странице список акансий у модератора"""
    vacancies_list = Vacancy.objects.exclude(status__status="NPB")
    if request.headers.get('x-requested-with') == 'XMLHttpRequest': # вместо отмершего if request.is_ajax()
        if stat == 'frv':
            vacancies_list = Vacancy.objects.filter(status__status="FRV")
        elif stat == 'all':
            vacancies_list = Vacancy.objects.exclude(status__status="NPB")
        elif stat == 'pub':
            vacancies_list = Vacancy.objects.filter(status__status="PUB")
        elif stat == 'rjc':
            vacancies_list = Vacancy.objects.filter(status__status="RJC")
        elif stat == 'apv':
            vacancies_list = Vacancy.objects.filter(status__status="APV")
        else:
            vacancies_list = Vacancy.objects.exclude(status__status="NPB")
    context = { 'vacancies_list': vacancies_list }
    result = render_to_string('vac_list.html', context)

    return JsonResponse({'result':result})
