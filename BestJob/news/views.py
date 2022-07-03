from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DeleteView, DetailView

from BestJob.settings import NEWS_BODY_LEN_ON_NEWS_LIST
from news.forms import NewsCreateForm, NewsUpdateForm#, NewsDeleteForm
from news.models import News
from search.models import Category


class IndexView(TemplateView):
    """view главной страницы с новостями"""
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        news_list = News.objects.filter(is_active=True).order_by('-created')

        if news_list:
            if len(news_list) >= 3:
                #  Берём top 3.
                context['news_list'] = news_list[:3]

        context['categories'] = Category.objects.all().order_by('name')
        return context


class NewsListView(ListView):
    """view главной страницы с новостями"""
    paginate_by = 3
    template_name = 'news_list.html'
    queryset = News.objects.filter(is_active=True).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        queryset = context['object_list']
        object_list = list()
        for item in queryset:
            if len(item.body) > NEWS_BODY_LEN_ON_NEWS_LIST:
                item.body = item.body[0:NEWS_BODY_LEN_ON_NEWS_LIST - 3] + '...'

            object_list.append(item)

        context['object_list'] = object_list
        return context


class NewsDetailView(DetailView):
    """view главной страницы с новостями"""
    model = News
    template_name = 'news_detail.html'

    def get(self, request, *args, **kwargs):
        super(NewsDetailView, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        news_id = kwargs.get('pk')
        try:
            news = News.objects.get(id=news_id)
            context['news_object'] = news
        except Exception:
            print(f'News not exists')

        return self.render_to_response(context)


class NewsModerateList(TemplateView):
    """view главной страницы с новостями"""
    template_name = 'news_moderate_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsModerateList, self).get_context_data(**kwargs)
        context['news_list'] = News.objects.all().order_by('-created')
        context['title'] = "Модерация новостей"
        context['heading'] = "Модерация новостей"
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

