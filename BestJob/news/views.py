from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

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
        context['title'] = 'Список новостей'
        context['heading'] = 'Список новостей'
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

        context['title'] = "Просмотр новости"
        context['heading'] = "Просмотр новости"

        return self.render_to_response(context)


class NewsModerateList(ListView):
    """view страницы для модерации новостей"""
    paginate_by = 3
    template_name = 'news_list.html'
    queryset = News.objects.order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsModerateList, self).get_context_data(**kwargs)
        queryset = context['object_list']
        object_list = list()
        for item in queryset:
            if len(item.body) > NEWS_BODY_LEN_ON_NEWS_LIST:
                item.body = item.body[0:NEWS_BODY_LEN_ON_NEWS_LIST - 3] + '...'

            object_list.append(item)

        context['title'] = "Модерация новостей"
        context['heading'] = "Модерация новостей"
        context['object_list'] = object_list
        return context


class NewsCreate(CreateView):
    """view для создания новостей"""
    model = News
    template_name = 'news_create.html'
    form_class = NewsCreateForm
    success_url = reverse_lazy('news:update_news')

    def get_context_data(self, **kwargs):
        context = super(NewsCreate, self).get_context_data(**kwargs)
        context['title'] = 'Создание Новости'
        context['heading'] = "Создание Новости"
        return context

    def form_valid(self, form):
        form.save()
        return super(NewsCreate, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
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
            messages.success(request, 'Новость успешно создана!')
            return redirect('news:update_news', pk=news.pk)
        else:
            print(form.errors)
            messages.error(request, 'Проверьте правильность заполнения новости!')
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

        if form.is_valid():
            if not form.has_changed():
                messages.error(request, 'Для сохранения измените хотя бы одно поле!')
                return self.form_invalid(form)
            form.save()
            messages.success(request, 'Новость успешно отредактирована!')
            return redirect(reverse("news:update_news", args=(news_id,)))
        else:
            print(form.errors)
            messages.error(request, 'Проверьте правильность заполнения новости!')
        return self.form_invalid(form)


class NewsDelete(DeleteView):
    """view для удаления новостей"""
    model = News

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            if user.role_id == UserRole.MODERATOR:
                self.object = self.get_object()
                self.object.delete()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        return HttpResponseForbidden()
