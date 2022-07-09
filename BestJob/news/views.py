from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils.datetime_safe import datetime
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DeleteView, DetailView

from BestJob.settings import NEWS_BODY_LEN_ON_NEWS_LIST, UserRole
from users.models import ModeratorProfile, User
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

        context['roles'] = UserRole
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
        form.save()
        return super(NewsCreate, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        author_id = request.user.pk
        form = self.form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            # сохраняем новую новость
            news = form.save(commit=False)
            news.author = ModeratorProfile.objects.get(id=author_id)
            news.title = form.data['title']
            news.body = form.data['body']
            news.image = form.instance.image
            news.save()
            return redirect(self.success_url)
        else:
            print(form.errors)
        return self.form_invalid(form)


class NewsUpdate(UpdateView):
    """view для обновления новостей"""
    model = News
    template_name = 'news_update.html'
    form_class = NewsUpdateForm
    success_url = reverse_lazy('news:moderate_news')

    def get_object(self, queryset=None):
        news_id = self.kwargs['pk']
        news = News.objects.filter(id=news_id)

        if news:
            return news.first()
        else:
            news = News()
            News.id = news.objects.get(pk=news_id)
            return news

    def get_context_data(self, **kwargs):
        context = super(NewsUpdate, self).get_context_data(**kwargs)
        context['title'] = "Редактирование новости"
        context['heading'] = "Редактирование новости"
        return context

    def get(self, request, *args, **kwargs):
        super(NewsUpdate, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        try:
            news_id = kwargs.get('pk')
            news = News.objects.get(id=news_id)
            context['news'] = news
            context['title'] = news.title
            context['body'] = news.body
            context['image'] = news.image
        except Exception:
            print(f'News {request.news.pk} not exists')
        context['news_list'] = News.objects.all()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object, files=request.FILES)
        news_id = self.kwargs['pk']

        news = News.objects.filter(id=news_id)

        if news:
            news = news.first()

            form.instance.pk = news.id
            form.instance.title = news.title
            form.instance.body = news.body

            if form.instance.image.closed:
                form.instance.image = news.image

        else:
            form.instance.news_id = news_id
            form.instance.user = News.objects.get(pk=news_id)
        form.save()
        return redirect(self.success_url)


class NewsDelete(DeleteView):
    """view для удаления новостей"""
    model = News
    template_name = 'news_confirm_delete.html'
    success_url = reverse_lazy('news:moderate_news')

    def form_valid(self, form):
        """Новость удаляется"""
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)
