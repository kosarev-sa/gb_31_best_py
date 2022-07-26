from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse, resolve
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView, ListView

from BestJob.mixin import BaseClassContextMixin
from BestJob.settings import UserRole
from approvals.models import ApprovalStatus

from cvs.forms import CVCreateForm, CVUpdateForm, CVDeleteForm, CVDistributeForm, ExperienceCreateForm, \
    EducationCreateForm, LanguagesCreateForm, ModeratorCVUpdateForm, LanguagesUpdateForm
from cvs.models import CV, Experience, CVWorkSchedule, CVEmployment, Education, LanguagesSpoken, CVMonths

from search.models import Category, Currency, Employments, WorkSchedules, Languages, LanguageLevels, EducationLevel
from users.models import WorkerProfile, EmployerProfile
from vacancies.models import Vacancy


class CVList(TemplateView):
    """view список резюме соискателя"""
    template_name = 'cv_list.html'
    list_of_cvs = CV.objects.all()

    def get(self, request, *args, **kwargs):
        super(CVList, self).get(request, *args, **kwargs)
        user_id = request.user.pk
        worker_id = WorkerProfile.objects.get(user=user_id)
        context = {
            'cvs': CV.objects.filter(worker_profile=worker_id, is_active=True),
            'worker': worker_id,
            'title': "Мои резюме",
            'heading': "Мои резюме",
        }
        return self.render_to_response(context)


class ModeratorCVList(TemplateView):
    """view просмотра вакансий модератором"""
    template_name = 'moderator_cvs_list.html'

    def get(self, request, *args, **kwargs):
        super(ModeratorCVList, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        context['cvs_list'] = CV.objects.filter(status__status="PUB").exclude(
            is_active=False).order_by('date_create')
        context['title'] = 'Модерация резюме'
        context['heading'] = "Модерация резюме"
        return self.render_to_response(context)


class ModeratorCVUpdate(UpdateView):
    """view изменения вакансий"""
    model = CV
    template_name = 'cv_detail.html'
    form_class = ModeratorCVUpdateForm
    success_url = reverse_lazy('cv:moderator_cvs_list')

    def get(self, request, *args, **kwargs):
        super(ModeratorCVUpdate, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        cv_id = self.kwargs['pk']
        cv = CV.objects.get(id=cv_id)
        context['object'] = cv

        '''Разделение строки навыки на пункты и передача в контекст списком'''
        skills = cv.skills.split(', ')
        context['skills'] = skills

        experience = Experience.objects.filter(cv=cv)
        context['experience'] = experience
        context['educations'] = Education.objects.filter(cv=cv)
        context['langlevels'] = LanguagesSpoken.objects.filter(cv=cv)
        cv_employments = [cv_empl.employment_id for cv_empl in CVEmployment.objects.filter(cv=cv)]
        employments = []
        for el in cv_employments:
            employment = Employments.objects.filter(id=el).first()
            employments.append(employment)
        context['employments'] = employments
        cv_schedules = [cv_sch.schedule_id for cv_sch in CVWorkSchedule.objects.filter(cv=cv)]
        schedules = []
        for el in cv_schedules:
            schedule = WorkSchedules.objects.filter(id=el).first()
            schedules.append(schedule)
        context['schedules'] = schedules
        context['is_moderating'] = True
        context['title'] = 'Модерация резюме'
        context['heading'] = "Модерация резюме"
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        cv_id = self.kwargs['pk']
        if form.is_valid():
            CV.objects.filter(pk=cv_id).update(status=form.instance.status,
                                               moderators_comment=form.instance.moderators_comment)
        else:
            print(form.errors)
        return redirect(self.success_url)


class CVCreate(CreateView):
    """view создание резюме"""
    model = CV
    template_name = 'cv_create.html'
    form_class = CVCreateForm
    success_url = 'cv:update_cv'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CVCreate, self).get_context_data(**kwargs)
        context['title'] = 'Создание резюме'
        context['heading'] = "Создание резюме"

        return context

    def get(self, request, *args, **kwargs):
        super(CVCreate, self).get(request, *args, **kwargs)
        worker = WorkerProfile.objects.get(user=request.user.pk)
        context = self.get_context_data()
        context['worker'] = worker
        context['employments'] = Employments.objects.all()
        context['schedules'] = WorkSchedules.objects.all()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = None
        worker = WorkerProfile.objects.get(user=request.user.pk)
        start_status = ApprovalStatus.objects.get(status='NPB')
        form = self.form_class(data=request.POST)
        if form.is_valid():
            # сохраняем новое резюме
            cv = form.save(commit=False)
            cv.worker_profile = worker
            cv.status = start_status
            cv.about = form.data['about']
            cv.save()

            for key, value in form.data.items():
                if key.startswith('schedule_'):
                    schedule = WorkSchedules.objects.get(code=value)
                    cv_schedule = CVWorkSchedule(cv=cv, schedule=schedule)
                    cv_schedule.save()

                elif key.startswith('empl_'):
                    employment = Employments.objects.get(code=value)
                    cv_employment = CVEmployment(cv=cv, employment=employment)
                    cv_employment.save()

            #   Нажата кнопка Добавить опыт работы
            if request.POST.get('experience', None):
                return redirect('cv:create_experience', pk=cv.id)
            #   Нажата кнопка Добавить место обучения
            if request.POST.get('education', None):
                return redirect('cv:create_education', cv_id=cv.id)

            if request.POST.get('language', None):
                return redirect('cv:create_language', cv_id=cv.id)

            messages.success(request, 'Резюме успешно создано!')
            return redirect(self.success_url, pk=cv.id)
        else:
            print(form.errors)
            messages.error(request, 'Проверьте правильность заполнения резюме!')
        return self.form_invalid(form)


class CVUpdate(UpdateView):
    """view изменение резюме"""
    model = CV
    template_name = 'cv_update.html'
    form_class = CVUpdateForm
    success_url = reverse_lazy('cv:update_cv')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CVUpdate, self).get_context_data(**kwargs)
        context['title'] = "Изменение резюме"
        context['heading'] = "Изменение резюме"

        return context

    def get(self, request, *args, **kwargs):
        super(CVUpdate, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        cv_id = kwargs.get('pk')
        cv = CV.objects.get(id=cv_id)
        worker = WorkerProfile.objects.get(user=request.user.pk)
        context['cv_id'] = cv.id
        context['worker'] = worker
        context['speciality'] = Category.objects.all().order_by('name')
        context['experience'] = Experience.objects.filter(cv=cv)
        context['educations'] = Education.objects.filter(cv=cv)
        context['langlevels'] = LanguagesSpoken.objects.filter(cv=cv)
        cv_employments = [cv_empl.employment_id for cv_empl in CVEmployment.objects.filter(cv=cv)]
        context['cv_employments'] = cv_employments
        context['employments'] = Employments.objects.all()
        cv_schedules = [cv_sch.schedule_id for cv_sch in CVWorkSchedule.objects.filter(cv=cv)]
        context['cv_schedules'] = cv_schedules
        context['schedules'] = WorkSchedules.objects.all()
        context['moderators_comment'] = cv.moderators_comment
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)

        if form.is_valid():
            # if not form.has_changed():
            #     messages.error(request, 'Для сохранения измените хотя бы одно поле!')
            #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            self.object.save()

            cv_schedules = CVWorkSchedule.objects.filter(cv=self.object)
            cv_schedules.delete()
            cv_employments = CVEmployment.objects.filter(cv=self.object)
            cv_employments.delete()

            for key, value in form.data.items():
                if key.startswith('schedule_'):
                    schedule = WorkSchedules.objects.get(code=value)
                    cv_schedule = CVWorkSchedule(cv=self.object, schedule=schedule)
                    cv_schedule.save()
                elif key.startswith('empl_'):
                    employment = Employments.objects.get(code=value)
                    cv_employment = CVEmployment(cv=self.object, employment=employment)
                    cv_employment.save()
            messages.success(request, 'Резюме успешно отредактировано!')
            return redirect(reverse('cv:update_cv', args=(kwargs.get('pk'),)))
        else:
            print(form.errors)

            # Generate errors string.
            error_string = str()
            for field, errors in form.errors.items():

                model_field = CV._meta.get_field(field)
                if model_field:
                    field_verbose_name = model_field.verbose_name
                    if field_verbose_name:
                        field = field_verbose_name

                error_string += f'{field}: {",".join(errors)}'

            messages.error(request, f'Проверьте правильность заполнения резюме!\n{error_string}')
            # return self.form_invalid(form)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class CVDelete(DeleteView):
    """view удаление резюме"""
    model = CV
    template_name = 'cv_delete.html'
    form_class = CVDeleteForm
    success_url = reverse_lazy('cv:cv_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CVDelete, self).get_context_data(**kwargs)

        cv_id = self.kwargs['pk']
        cv = CV.objects.get(id=cv_id)

        context['object'] = cv
        context['title'] = "Удаление резюме"
        context['heading'] = "Удаление резюме"

        return context

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CVDetailView(DetailView):
    """view просмотр резюме"""
    model = CV
    template_name = 'cv_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CVDetailView, self).get_context_data(**kwargs)

        cv_id = self.kwargs['pk']
        cv = CV.objects.get(id=cv_id)
        context['object'] = cv

        '''Разделение строки навыки на пункты и передача в контекст списком'''
        skills = cv.skills.split(', ')
        context['skills'] = skills

        experience = Experience.objects.filter(cv=cv)
        # '''Разделение строки обязанности на пункты и передача в контекст списком'''
        # for el in experience:
        #     responsibilities = el.responsibilities.split(', ')
        #     el.responsibilities = responsibilities
        context['experience'] = experience

        context['educations'] = Education.objects.filter(cv=cv)
        context['langlevels'] = LanguagesSpoken.objects.filter(cv=cv)
        cv_employments = [cv_empl.employment_id for cv_empl in CVEmployment.objects.filter(cv=cv)]
        employments = []
        for el in cv_employments:
            employment = Employments.objects.filter(id=el).first()
            employments.append(employment)
        context['employments'] = employments

        cv_schedules = [cv_sch.schedule_id for cv_sch in CVWorkSchedule.objects.filter(cv=cv)]
        schedules = []
        for el in cv_schedules:
            schedule = WorkSchedules.objects.filter(id=el).first()
            schedules.append(schedule)
        context['schedules'] = schedules
        context['is_moderating'] = False

        context['title'] = "Резюме"
        context['heading'] = "Резюме"

        return context

    def get(self, request, *args, **kwargs):
        super(CVDetailView, self).get(request, *args, **kwargs)
        context = self.get_context_data(object_list=None, **kwargs)

        if request.user.role_id == UserRole.WORKER:
            context['worker'] = True
        elif request.user.role_id == UserRole.EMPLOYER:
            context['employer'] = EmployerProfile.objects.get(user=request.user)
        return self.render_to_response(context)


def set_public_status(request, pk):
    cv = get_object_or_404(CV, pk=pk)
    cv.status = ApprovalStatus.objects.get(status='PUB')
    cv.save()
    return HttpResponseRedirect(reverse('cv:cv_list'))


class CVExperienceCreate(CreateView):
    """Создание опыта работы"""
    model = Experience
    template_name = 'cv_experience.html'
    form_class = ExperienceCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Место работы'
        context['months'] = CVMonths
        context['cv_id'] = self.kwargs['pk']
        context['title'] = "Добавление места работы"
        context['heading'] = "Добавление места работы"

        return context

    def get(self, request, *args, **kwargs):
        super(CVExperienceCreate, self).get(request, *args, **kwargs)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = None
        cv = CV.objects.get(id=self.kwargs.get('pk'))
        form = self.form_class(data=request.POST)
        if form.is_valid():
            # сохраняем новый так сказать опыт)
            experience = form.save(commit=False)
            experience.cv = cv
            experience.save()
            messages.success(request, 'Опыт работы добавлен!')
            return redirect('cv:update_cv', pk=cv.id)
        else:
            # messages.error(request, form.errors)
            print(form.errors)
            messages.error(request, 'Проверьте правильность заполнения формы!')
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            return self.form_invalid(form)


class CVExperienceUpdate(UpdateView):
    """Изменение опыта работы"""
    model = Experience
    template_name = 'cv_experience.html'
    form_class = ExperienceCreateForm
    success_url = reverse_lazy('cv:cv_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Место работы'
        context['months'] = CVMonths
        exp = Experience.objects.get(id=self.kwargs.get('pk'))
        context['cv_id'] = exp.cv.id
        context['title'] = "Изменение места работы"
        context['heading'] = "Изменение места работы"

        return context

    def get(self, request, *args, **kwargs):
        super(CVExperienceUpdate, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        # exp = Experience.objects.get(id=self.kwargs.get('pk'))
        # context['cv_id'] = exp.cv.id
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        super(CVExperienceUpdate, self).post(request, *args, **kwargs)
        self.object = self.get_object()
        form = self.form_class(data=request.POST, instance=self.object)
        if form.is_valid():
            # if not form.has_changed():
            #     messages.error(request, 'Для сохранения измените хотя бы одно поле!')
            #     return self.form_invalid(form)
            messages.success(request, 'Опыт работы обновлён!')
            return redirect('cv:update_cv', pk=self.object.cv.id)
        else:
            # messages.error(request, form.errors)
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            messages.error(request, 'Проверьте правильность заполнения формы!')
            return self.form_invalid(form)


class CVExperienceDelete(DeleteView):
    """Удаление опыта работы без поднятия формы"""
    model = Experience

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # Раскоментировать, если будет шаблон на удаление
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Удаление места работы'
    #     context['heading'] = "Удаление места работы"
    #
    #     return context


class CVEducationCreate(CreateView):
    """Создание места обучения"""
    model = Education
    template_name = 'cv_education.html'
    form_class = EducationCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление места обучения'
        context['cv_id'] = self.kwargs['cv_id']
        context['heading'] = "Добавление места обучения"
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        cv = CV.objects.get(id=self.kwargs.get('cv_id'))
        form = self.form_class(data=request.POST)
        if form.is_valid():
            # сохраняем новое место обучения
            education = form.save(commit=False)
            education.cv = cv
            education.save()
            messages.success(request, 'Обучение успешно добавлено!')
            return redirect('cv:update_cv', pk=cv.id)
        else:
            # messages.error(request, form.errors)
            print(form.errors)
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            messages.error(request, 'Проверьте правильность заполнения формы!')
            return self.form_invalid(form)


class CVEducationUpdate(UpdateView):
    """Редактирование места обучения"""
    model = Education
    template_name = 'cv_education.html'
    form_class = EducationCreateForm
    success_url = reverse_lazy('cv:cv_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение места обучения'
        educ = Education.objects.get(id=self.kwargs.get('pk'))
        context['cv_id'] = educ.cv.id
        context['heading'] = 'Изменение места обучения'
        return context

    def post(self, request, *args, **kwargs):
        super(CVEducationUpdate, self).post(request, *args, **kwargs)
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            # if not form.has_changed():
            #     messages.error(request, 'Для сохранения измените хотя бы одно поле!')
            #     return self.form_invalid(form)
            messages.success(request, 'Информация об обучении обновлена!')
            return redirect('cv:update_cv', pk=self.object.cv.id)
        else:
            # messages.error(request, form.errors)
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            messages.error(request, 'Проверьте правильность заполнения формы!')
            return self.form_invalid(form)


class CVEducationDelete(DeleteView):
    """Удаление места обучения без поднятия формы"""
    model = Education

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class CVLanguageCreate(CreateView):
    """Создание вледения языком"""
    model = LanguagesSpoken
    template_name = 'cv_languages.html'
    form_class = LanguagesCreateForm
    success_url = reverse_lazy('cv:cv_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Владение языком'
        context['cv_id'] = self.kwargs['cv_id']
        context['heading'] = 'Знание языка'
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        cv = CV.objects.get(id=self.kwargs.get('cv_id'))
        form = self.form_class(data=request.POST)
        if form.is_valid():
            # сохраняем новый язык
            language = form.save(commit=False)
            language.cv = cv
            language.save()
            messages.success(request, 'Информация о языке добавлена!')
            return redirect('cv:update_cv', pk=cv.id)
        else:
            # messages.error(request, form.errors)
            print(form.errors)
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            messages.error(request, 'Проверьте правильность заполнения формы!')
            return self.form_invalid(form)


class CVLanguageUpdate(UpdateView):
    """Изменение вледения языком"""
    model = LanguagesSpoken
    template_name = 'cv_languages.html'
    form_class = LanguagesUpdateForm
    success_url = reverse_lazy('cv:cv_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Владение языком'
        lang = LanguagesSpoken.objects.get(id=self.kwargs.get('pk'))
        context['cv_id'] = lang.cv.id
        context['heading'] = 'Знание языка'
        return context

    def post(self, request, *args, **kwargs):
        super(CVLanguageUpdate, self).post(request, *args, **kwargs)
        self.object = self.get_object()
        form = self.form_class(data=request.POST, instance=self.object)
        if form.is_valid():
            # if not form.has_changed():
            #     messages.error(request, 'Для сохранения измените хотя бы одно поле!')
            #     return self.form_invalid(form)
            messages.success(request, 'Информация о языке обновлена!')
            return redirect('cv:update_cv', pk=self.object.cv.id)
        else:
            # messages.error(request, form.errors)
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            messages.error(request, 'Проверьте правильность заполнения формы!')
            return self.form_invalid(form)


class CVLanguageDelete(DeleteView):
    """Удаление вледения языком без формы"""
    model = LanguagesSpoken

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def edit_cv_list(request, stat):
    """Обновление списка резюме соглано статусу на странице список резюме у модератора"""
    cvs_list = CV.objects.exclude(status__status="NPB")

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # вместо отмершего if request.is_ajax()
        if stat == 'frv':
            cvs_list = CV.objects.filter(status__status="FRV").exclude(
                is_active=False).order_by('date_create')
        elif stat == 'all':
            cvs_list = CV.objects.exclude(status__status="NPB").exclude(
                is_active=False).order_by('-date_create')
        elif stat == 'pub':
            cvs_list = CV.objects.filter(status__status="PUB").exclude(
                is_active=False).order_by('date_create')
        elif stat == 'rjc':
            cvs_list = CV.objects.filter(status__status="RJC").exclude(
                is_active=False).order_by('-date_create')
        elif stat == 'apv':
            cvs_list = CV.objects.filter(status__status="APV").exclude(
                is_active=False).order_by('-date_create')
        else:
            cvs_list = CV.objects.exclude(status__status="NPB").exclude(
                is_active=False).order_by('-date_create')
    context = {'cvs_list': cvs_list}
    result = render_to_string('cvs_list.html', context)

    return JsonResponse({'result': result})


class RecomendedCVList(ListView, BaseClassContextMixin):
    """view просмотра рекомендованных по вакансии резюме """
    template_name = 'cv_list.html'
    model = CV
    title = 'BestJob | Рекомендованные вакансии'

    def get(self, request, *args, **kwargs):
        super(RecomendedCVList, self).get(request, *args, **kwargs)
        vacancy = Vacancy.objects.get(id=self.kwargs['pk'])
        employer = vacancy.employer_profile
        context = {
            'cvs': CV.objects.filter(speciality=vacancy.specialization).exclude(
                status__status="NPB").exclude(status__status="RJC").exclude(
                is_active=False),
            'title': "Рекомендованные резюме",
            'heading': "Рекомендованные резюме",
            'employer': employer
            # Сделать переход в шапке, куда?
            # 'link': "",
            # 'heading_link': "",
        }

        return self.render_to_response(context)
