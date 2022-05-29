from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView

from news.forms import NewsCreateForm, NewsUpdateForm, NewsDeleteForm
from news.models import News


class NewsView(TemplateView):
    """view главной страницы с новостями"""
    template_name = 'news.html'
    list_of_news = News.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsView, self).get_context_data(**kwargs)
        context['news'] = self.list_of_news
        return context


class NewsModerateList(TemplateView):
    """view главной страницы с новостями"""
    template_name = 'news_moderate_list.html'
    list_of_news = News.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsModerateList, self).get_context_data(**kwargs)
        context['news'] = self.list_of_news
        return context


class NewsCreate(CreateView):
    """view для создания новостей"""
    model = News
    template_name = 'news_create.html'
    form_class = NewsCreateForm
    success_url = reverse_lazy('news:moderate_news')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsCreate, self).get_context_data(**kwargs)
        return context


class NewsUpdate(UpdateView):
    """view для обновления новостей"""
    model = News
    template_name = 'news_update.html'
    form_class = NewsUpdateForm
    success_url = reverse_lazy('news:moderate_news')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsUpdate, self).get_context_data(**kwargs)
        return context


class NewsDelete(UpdateView):
    """view для обновления новостей"""
    model = News
    template_name = 'news_delete.html'
    form_class = NewsDeleteForm
    success_url = reverse_lazy('news:moderate_news')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsDelete, self).get_context_data(**kwargs)
        return context
