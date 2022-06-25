from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DeleteView

from news.forms import NewsCreateForm, NewsUpdateForm#, NewsDeleteForm
from news.models import News
from search.models import Category


class NewsView(TemplateView):
    """view главной страницы с новостями"""
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsView, self).get_context_data(**kwargs)
        news_list = News.objects.filter(is_active=True).order_by('-created')

        if len(news_list) >= 3:
            #  Берём top 3.
            context['news_list'] = news_list[:3]

        context['categories'] = Category.objects.all().order_by('name')
        return context


class NewsModerateList(TemplateView):
    """view главной страницы с новостями"""
    template_name = 'news_moderate_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsModerateList, self).get_context_data(**kwargs)
        context['news_list'] = News.objects.all().order_by('-created')
        return context


class NewsCreate(CreateView):
    """view для создания новостей"""
    model = News
    template_name = 'news_create.html'
    form_class = NewsCreateForm
    success_url = reverse_lazy('news:moderate_news')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(NewsCreate, self).form_valid(form)


class NewsUpdate(UpdateView):
    """view для обновления новостей"""
    model = News
    template_name = 'news_update.html'
    form_class = NewsUpdateForm
    success_url = reverse_lazy('news:moderate_news')

    def get_context_data(self, **kwargs):
        context = super(NewsUpdate, self).get_context_data(**kwargs)
        return context


class NewsDelete(DeleteView):
    """view для удаления новостей"""
    model = News
    template_name = 'news_confirm_delete.html'
    success_url = reverse_lazy('news:moderate_news')

    # def form_valid(self, form):
    #     """Новость не удаляется, а делается не активной"""
    #     success_url = self.get_success_url()
    #     self.object.is_active = False
    #     self.object.save()
    #     return HttpResponseRedirect(success_url)

