from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from approvals.models import ApprovalStatus
from cvs.forms import CVCreateForm, CVUpdateForm, CVDeleteForm, CVDistributeForm
from cvs.models import CV, Experience, CVWorkSchedule, CVEmployment, Education, LanguagesSpoken
from search.models import Category, Currency, Employments, WorkSchedules, Languages, LanguageLevels
from users.models import WorkerProfile



def save_experience (data, cv):
    experience = Experience(cv=cv)
    experience.name = data.get('name_exp')
    experience.month_begin = data.get('month_begin', 1)
    experience.year_begin = data.get('year_begin')
    experience.month_end = data.get('month_end', 1)
    experience.year_end = data.get('year_end')
    experience.post = data.get('post_exp')
    experience.responsibilities = data.get('responsibilities')
    experience.save()


def save_education(data, cv):
    education = Education(cv=cv)
    education.date_end = data.get('educ_end')
    education.name = data.get('educ_name')
    education.department = data.get('department')
    education.specialty = data.get('educ_specialty')
    education.save()


def save_languages( data, cv):
    level = LanguageLevels.objects.get(code=data.get('level'))
    language = Languages.objects.get(code=data.get('lang'))
    language_level = LanguagesSpoken(cv=cv, language=language, level=level)
    language_level.save()


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
            'worker': worker_id
        }
        return self.render_to_response(context)


class CVCreate(CreateView):
    """view создание резюме"""
    model = CV
    template_name = 'cv_create.html'
    form_class = CVCreateForm
    success_url = reverse_lazy('cv:cv_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CVCreate, self).get_context_data(**kwargs)
        context['title'] = 'Новое резюме'
        return context

    def get(self, request, *args, **kwargs):
        super(CVCreate, self).get(request, *args, **kwargs)
        worker = WorkerProfile.objects.get(user=request.user.pk)
        context = self.get_context_data()
        context['worker'] = worker
        context['speciality'] = Category.objects.all().order_by('name')
        context['employments'] = Employments.objects.all()
        context['schedules'] = WorkSchedules.objects.all()
        context['languages'] = Languages.objects.all()
        context['levels'] = LanguageLevels.objects.all()
        context['months'] = Experience.Month
        return self.render_to_response(context)


    def post(self, request, *args, **kwargs):
        worker = WorkerProfile.objects.get(user=request.user.pk)
        start_status = ApprovalStatus.objects.get(status='CHG')
        form = self.form_class(data=request.POST)
        if form.is_valid():
            # сохраняем новое резюме
            cv = form.save(commit=False)
            cv.worker_profile = worker
            cv.status = start_status
            cv.save()
            # сохраняем опыт работы
            if form.data.get('name_exp', None):
                save_experience(form.data, cv)
            # сохраняем образование
            if form.data.get('educ_name', None):
                save_education(form.data, cv)
            # язык
            if form.data.get('lang', None):
                save_languages(form.data, cv)

            for key, value in form.data.items():
                if key.startswith('schedule_'):
                    schedule = WorkSchedules.objects.get(code=value)
                    cv_schedule = CVWorkSchedule(cv=cv, schedule=schedule)
                    cv_schedule.save()
                elif key.startswith('empl_'):
                    employment = Employments.objects.get(code=value)
                    cv_employment = CVEmployment(cv=cv, employment=employment)
                    cv_employment.save()

            return redirect(self.success_url)
        else:
            print(form.errors)
        return self.form_invalid(form)


class CVUpdate(UpdateView):
    """view изменение резюме"""
    model = CV
    template_name = 'cv_update.html'
    form_class = CVUpdateForm
    success_url = reverse_lazy('cv:cv_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CVUpdate, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        super(CVUpdate, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        cv_id = kwargs.get('pk')
        cv = CV.objects.get(id=cv_id)
        worker = WorkerProfile.objects.get(user=request.user.pk)
        context['worker'] = worker
        context['speciality'] = Category.objects.all().order_by('name')
        context['experience'] = Experience.objects.filter(cv=cv)
        context['educations'] = Education.objects.filter(cv=cv)
        context['langlevels'] = LanguagesSpoken.objects.filter(cv=cv)
        context['languages'] = Languages.objects.all()
        context['levels'] = LanguageLevels.objects.all()
        cv_employments = [cv_empl.employment_id for cv_empl in CVEmployment.objects.filter(cv=cv)]
        context['cv_employments'] = cv_employments
        context['employments'] = Employments.objects.all()
        cv_schedules = [cv_sch.schedule_id for cv_sch in CVWorkSchedule.objects.filter(cv=cv)]
        context['cv_schedules'] = cv_schedules
        context['schedules'] = WorkSchedules.objects.all()
        return self.render_to_response(context)


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)

        if form.is_valid():
            self.object.save()
            if form.data.get('name_exp', None):
                exp = Experience.objects.filter(cv=self.object)
                exp.delete()
                save_experience(form.data, self.object)
                # сохраняем образование
            if form.data.get('educ_name', None):
                educ = Education.objects.filter(cv=self.object)
                educ.delete()
                save_education(form.data, self.object)
                # язык
            if form.data.get('lang', None):
                lang = LanguagesSpoken.objects.filter(cv=self.object)
                lang.delete()
                save_languages(form.data, self.object)

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
            return redirect(self.success_url)
        else:
            print(form.errors)
        return self.form_invalid(form)



class CVDelete(DeleteView):
    """view удаление резюме"""
    model = CV
    template_name = 'cv_delete.html'
    form_class = CVDeleteForm
    success_url = reverse_lazy('cv:cv_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CVDelete, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CVDistribute(UpdateView):
    """view для размещения резюме"""
    model = CV
    template_name = 'cv_distribute.html'
    form_class = CVDistributeForm
    success_url = reverse_lazy('cv:cv_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CVDistribute, self).get_context_data(**kwargs)
        return context
