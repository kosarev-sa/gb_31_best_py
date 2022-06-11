from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from cvs.forms import CVCreateForm, CVUpdateForm, CVDeleteForm, CVDistributeForm
from cvs.models import CV
from search.models import Category, Currency, Employments, WorkSchedules
from users.models import WorkerProfile


class CVList(TemplateView):
    """view список резюме соискателя"""
    template_name = 'cv_list.html'
    list_of_cvs = CV.objects.all()

    def get(self, request, *args, **kwargs):
        super(CVList, self).get(request, *args, **kwargs)
        user_id = request.user.pk
        worker_id = WorkerProfile.objects.get(user=user_id)
        context = {
            'cvs': CV.objects.filter(worker_profile=worker_id),
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
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        worker = WorkerProfile.objects.get(user=request.user.pk)
        form = self.form_class(data=request.POST)
        if form.is_valid():
            # сохраняем новое резюме
            cv = form.save(commit=False)
            cv.worker_profile = worker
            cv.save()
            # отправляем email с подтверждением почты
            # self.send_verify_link(cv)
            # создаем профиль в зависимости от роли
            # if user.role_id == 2:
            #     employer_profile = EmployerProfile(user_id=user.pk)
            #     employer_profile.save()
            # elif user.role_id == 3:
            #     worker_profile = WorkerProfile(user_id=user.pk)
            #     worker_profile.save()

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


class CVDelete(DeleteView):
    """view удаление резюме"""
    model = CV
    template_name = 'cv_delete.html'
    form_class = CVDeleteForm
    success_url = reverse_lazy('cv:cv_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CVDelete, self).get_context_data(**kwargs)
        return context


class CVDistribute(UpdateView):
    """view для обновления резюме"""
    model = CV
    template_name = 'cv_distribute.html'
    form_class = CVDistributeForm
    success_url = reverse_lazy('cv:cv_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CVDistribute, self).get_context_data(**kwargs)
        return context
