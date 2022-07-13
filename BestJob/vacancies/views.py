from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DeleteView, DetailView

from BestJob.settings import UserRole
from cvs.models import CV
from search.models import Category, Employments, WorkSchedules, Languages, \
    LanguageLevels
from vacancies.forms import VacancyCreateForm, VacancyUpdateForm, VacancyDistributeForm, ModeratorVacancyUpdateForm, \
    VacancyDeleteForm
from vacancies.models import Vacancy
from users.models import EmployerProfile, WorkerProfile
from approvals.models import ApprovalStatus

from BestJob.mixin import BaseClassContextMixin, UserDispatchMixin


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
            'status': ApprovalStatus.objects.get(status='APV'),
            'title': "Ваши вакансии",
            'heading': "Ваши вакансии",
            # 'link': "/vacancies/create/",
            # 'heading_link': "Создать вакансию",
        }
        return self.render_to_response(context)


class ModeratorVacancyList(TemplateView):
    """view просмотра вакансий модератором"""
    template_name = 'moderator_vacancy_list.html'

    def get(self, request, *args, **kwargs):
        super(ModeratorVacancyList, self).get(request, *args, **kwargs)

        context = self.get_context_data()
        context['title'] = 'Модерация вакансий'
        context['heading'] = 'Модерация вакансий'
        context['vacancies_list'] = Vacancy.objects.filter(status__status="PUB").exclude(
                is_active=False)

        return self.render_to_response(context)


class ModeratorVacancyUpdate(UpdateView):
    """view изменения вакансий"""
    model = Vacancy
    template_name = 'vacancy_detail.html'
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
        context['is_moderating'] = True
        context['title'] = 'Модерация вакансии'
        context['heading'] = 'Модерация вакансии'
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        vac_id = self.kwargs['pk']
        if form.is_valid():
            Vacancy.objects.filter(pk=vac_id).update(status=form.instance.status,
                                                     moderators_comment=form.instance.moderators_comment)
        else:
            print(form.errors)
        return redirect(self.success_url)


class VacancyCreate(CreateView):
    """view создания вакансий"""
    model = Vacancy
    template_name = 'vacancy_create.html'
    form_class = VacancyCreateForm
    success_url = 'vacancy:update_vacancy'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacancyCreate, self).get_context_data(**kwargs)
        context['title'] = 'Создание вакансии'
        context['heading'] = "Создание вакансии"
        # context['link'] = "/vacancies/all/"
        # context['heading_link'] = "Список вакансий"
        return context

    def get(self, request, *args, **kwargs):
        super(VacancyCreate, self).get(request, *args, **kwargs)
        employer = EmployerProfile.objects.get(user=request.user.pk)
        context = self.get_context_data()
        context['employer'] = employer
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object=None
        employer = EmployerProfile.objects.get(user=request.user.pk)
        start_status = ApprovalStatus.objects.get(status='NPB')
        form = self.form_class(data=request.POST, files=request.FILES)
        salary_on_hand = request.POST.get('id_salary_on_hand', False)
        is_active = request.POST.get('id_is_active', True)

        if form.is_valid():
            # сохраняем новую вакансию
            vacancy = form.save(commit=False)
            vacancy.employer_profile = employer
            vacancy.status = start_status
            vacancy.salary_on_hand = salary_on_hand
            vacancy.is_active = is_active
            vacancy.save()
            messages.success(request, 'Вакансия успешно создана!')
            return redirect(self.success_url, pk=vacancy.id)
        else:
            print(form.errors)
            messages.error(request, 'Проверьте правильность заполнения вакансии!')
        return self.form_invalid(form)


class VacancyUpdate(UpdateView):
    """view изменения вакансий"""
    model = Vacancy
    template_name = 'vacancy_update.html'
    form_class = VacancyUpdateForm
    success_url = reverse_lazy('vacancy:vacancy_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacancyUpdate, self).get_context_data(**kwargs)
        context['title'] = "Изменение вакансии"
        context['heading'] = "Изменение вакансии"

        return context

    def get(self, request, *args, **kwargs):
        super(VacancyUpdate, self).get(request, *args, **kwargs)
        self.object = self.get_object()
        context = self.get_context_data()
        # Временное решение до реализации get view для вакансии
        try:
            employer = EmployerProfile.objects.get(user=request.user.pk)
            context['employer'] = employer

        except Exception:
            print(f'Employer {request.user.pk} not exists')
        context['employments'] = Employments.objects.all()
        if self.object.status.status in ('FRV', 'RJC'):
            context['moderators_comment'] = self.object.moderators_comment
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        super(VacancyUpdate, self).post(request, *args, **kwargs)
        self.object = self.get_object()
        form = self.form_class(data=request.POST)  # ,instance=self.object)
        salary_on_hand = request.POST.get('id_salary_on_hand', False)
        # is_active = request.POST.get('id_is_active', False)
        if form.is_valid():
            self.object.is_active = True
            self.object.salary_on_hand = salary_on_hand
            self.object.save()
            # if not form.has_changed():
            #     messages.error(request, 'Для сохранения измените хотя бы одно поле!')
            #     return self.form_invalid(form)
            messages.success(request, 'Вакансия успешно отредактирована!')
            return redirect(self.success_url)
        else:
            # messages.error(request, form.errors)
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            print(form.errors)
            messages.error(request, 'Проверьте правильность заполнения вакансии!')
        return self.form_invalid(form)


class VacancyDelete(DeleteView):
    """view удаления вакансий"""
    model = Vacancy
    template_name = 'vacancy_delete.html'
    form_class = VacancyDeleteForm
    success_url = reverse_lazy('vacancy:vacancy_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacancyDelete, self).get_context_data(**kwargs)

        vacancy_id = self.kwargs['pk']
        vacancy = Vacancy.objects.get(id=vacancy_id)

        context['object'] = vacancy
        context['title'] = "Удаление вакансии"
        context['heading'] = "Удаление вакансии"

        return context

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class VacancyDistribute(UpdateView):
    """view для размещения вакансий"""
    model = Vacancy
    template_name = 'vacancy_distribute.html'
    form_class = VacancyDistributeForm
    success_url = reverse_lazy('vacancy:vacancy_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacancyDistribute, self).get_context_data(**kwargs)
        return context


def set_public_status(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    vacancy.status = ApprovalStatus.objects.get(status='PUB')
    vacancy.save()
    return HttpResponseRedirect(reverse('vacancy:vacancy_list'))


class VacancyOpenList(TemplateView, BaseClassContextMixin):
    """view просмотра активных вакансий любым пользователем"""
    template_name = 'vacancy_base.html'
    title = 'BestJob | Вакансии'

    def get(self, request, *args, **kwargs):
        super(VacancyOpenList, self).get(request, *args, **kwargs)
        context = {
            'vacancies': Vacancy.objects.filter(is_active=True).exclude(
                status__status="NPB").exclude(status__status="RJC")
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
        worker = cv.worker_profile
        context = {
            'vacancies': Vacancy.objects.filter(specialization=cv.speciality).exclude(
                status__status="NPB").exclude(status__status="RJC").exclude(
                is_active=False),
            'worker': worker,
            'title': "Рекомендованные вакансии",
            'heading': "Рекомендованные вакансии",
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
            context['title'] = "Вакансия"
            context['heading'] = "Вакансия"

        except Exception:
            print(f'Employer not exists')
        context['employments'] = Employments.objects.all()

        if request.user.role.id == UserRole.WORKER:
            worker = WorkerProfile.objects.get(user=request.user)
            context['worker'] = worker

        return self.render_to_response(context)


def edit_vacancy_list(request, stat):
    """Обновление списка вакансий соглано статусу на странице список акансий у модератора"""
    vacancies_list = Vacancy.objects.exclude(status__status="NPB").exclude(
                is_active=False)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # вместо отмершего if request.is_ajax()
        if stat == 'frv':
            vacancies_list = Vacancy.objects.filter(status__status="FRV").exclude(
                is_active=False)
        elif stat == 'all':
            vacancies_list = Vacancy.objects.exclude(status__status="NPB").exclude(
                is_active=False)
        elif stat == 'pub':
            vacancies_list = Vacancy.objects.filter(status__status="PUB").exclude(
                is_active=False)
        elif stat == 'rjc':
            vacancies_list = Vacancy.objects.filter(status__status="RJC").exclude(
                is_active=False)
        elif stat == 'apv':
            vacancies_list = Vacancy.objects.filter(status__status="APV").exclude(
                is_active=False)
        else:
            vacancies_list = Vacancy.objects.exclude(status__status="NPB").exclude(
                is_active=False)
    context = {'vacancies_list': vacancies_list}
    result = render_to_string('vac_list.html', context)

    return JsonResponse({'result': result})
