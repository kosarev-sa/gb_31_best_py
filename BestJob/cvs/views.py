from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from cvs.forms import CVCreateForm, CVUpdateForm, CVDeleteForm, CVDistributeForm
from cvs.models import CV


class CVList(TemplateView):
    """view главной страницы с новостями"""
    template_name = 'cv_list.html'
    list_of_news = CV.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CVList, self).get_context_data(**kwargs)
        context['news'] = self.list_of_news
        return context


class CVCreate(CreateView):
    """view для создания новостей"""
    model = CV
    template_name = 'cv_create.html'
    form_class = CVCreateForm
    success_url = reverse_lazy('cv:cv_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CVCreate, self).get_context_data(**kwargs)
        return context


class CVUpdate(UpdateView):
    """view для обновления новостей"""
    model = CV
    template_name = 'cv_update.html'
    form_class = CVUpdateForm
    success_url = reverse_lazy('cv:cv_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CVUpdate, self).get_context_data(**kwargs)
        return context


class CVDelete(DeleteView):
    """view для обновления новостей"""
    model = CV
    template_name = 'cv_delete.html'
    form_class = CVDeleteForm
    success_url = reverse_lazy('cv:cv_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CVDelete, self).get_context_data(**kwargs)
        return context


class CVDistribute(UpdateView):
    """view для обновления новостей"""
    model = CV
    template_name = 'cv_distribute.html'
    form_class = CVDistributeForm
    success_url = reverse_lazy('cv:cv_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CVDistribute, self).get_context_data(**kwargs)
        return context
