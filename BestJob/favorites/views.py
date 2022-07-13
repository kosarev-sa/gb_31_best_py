from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView

from BestJob.settings import UserRole
from cvs.models import CV
from .models import EmployerFavorites, WorkerFavorites
from relations.models import Relations
from users.models import WorkerProfile, EmployerProfile
from vacancies.models import Vacancy


def fav_emp_add_remove(request, cv_id):
    '''
    Добавление/Удаление избранного из поиска.
    :param request:
    :param cv_id:
    :return:
    '''
    if request.user.is_authenticated:
        user = request.user
        # Работодатель.
        if user.role_id == UserRole.EMPLOYER:
            employer_profile = EmployerProfile.objects.get(user=user)
            cv = CV.objects.get(pk=cv_id)
            ef = EmployerFavorites.objects.filter(employer_profile=employer_profile, cv=cv)
            if ef:
                ef.first().delete()
            else:
                new_fav = EmployerFavorites()
                new_fav.cv = cv
                new_fav.employer_profile = employer_profile
                new_fav.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def fav_work_add_remove(request, vacancy_id):
    '''
    Добавление/Удаление избранного из поиска.
    :param request:
    :param vacancy_id:
    :return:
    '''
    if request.user.is_authenticated:
        user = request.user
        # Соискатель.
        if user.role_id == UserRole.WORKER:
            worker_profile = WorkerProfile.objects.get(user=user)
            vacancy = Vacancy.objects.get(pk=vacancy_id)

            wf = WorkerFavorites.objects.filter(worker_profile=worker_profile, vacancy=vacancy)
            if wf:
                wf.first().delete()
            else:
                new_fav = WorkerFavorites()
                new_fav.vacancy = vacancy
                new_fav.worker_profile = worker_profile
                new_fav.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class FavoritesEmployerDeleteView(DeleteView):
    """view удаление избранного работадателя"""
    model = EmployerFavorites

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            if user.role_id == UserRole.EMPLOYER:
                self.object = self.get_object()
                self.object.delete()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        return HttpResponseForbidden()


class FavoritesWorkerDeleteView(DeleteView):
    """view удаление избранного соискателя"""
    model = WorkerFavorites

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            if user.role_id == UserRole.WORKER:
                self.object = self.get_object()
                self.object.delete()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        return HttpResponseForbidden()


class FavoritesWorkerListView(ListView):
    """view отображения избранного для работадателя"""
    paginate_by = 3
    template_name = 'favorites_list.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user

            if user.role_id == UserRole.WORKER:
                worker_profiles = WorkerProfile.objects.filter(user_id=user.pk)
                if worker_profiles:
                    profiler = worker_profiles.first()
                    worker_favorites = WorkerFavorites.objects.filter(
                        worker_profile=profiler).order_by('-created')

                    # Я ищу работу и у меня есть резюме. Мои резюме.
                    cvs = CV.objects.filter(worker_profile=profiler)

                    # Вычисление оправлялся ли отклик на вакансию из избранного.
                    for favorit in worker_favorites:

                        favorit.has_relaton = False

                        # Отправлял ли я отклик на вакансии из избранного?
                        for cv in cvs:
                            relations = Relations.objects.filter(cv=cv, vacancy=favorit.vacancy)
                            # Если relation, то отправлял.
                            if relations:
                                favorit.has_relaton = True
                                favorit.relations_id = relations.first().pk
                                break

                    return worker_favorites

    def get_context_data(self, **kwargs):
        context = super(FavoritesWorkerListView, self).get_context_data(**kwargs)
        context['title'] = "Избранное"
        context['heading'] = "Избранное"
        # context['link'] = "/"
        # context['heading_link'] = "На главную"
        context['is_worker'] = True

        if self.request.user.is_authenticated:
            user = self.request.user

            if user.role_id == UserRole.WORKER:
                worker_profiles = WorkerProfile.objects.filter(user_id=user.pk)
                if worker_profiles:
                    profiler = worker_profiles.first()

                    # Я ищу работу и у меня есть резюме. Мои резюме.
                    cvs = CV.objects.filter(worker_profile=profiler).exclude(status__status="NPB").\
                        exclude(status__status="RJC").exclude(is_active=False)

                    context['modal_header'] = 'Выбор резюме'
                    context['modal_combo'] = cvs
                    context['modal_combo_empty'] = 'Выберите резюме'

        else:
            error_message = f'user is not authenticated'
            context['error_message'] = error_message
            print(error_message)

        return context


class FavoritesEmployerListView(ListView):
    """view отображения избранного для соискателя"""
    paginate_by = 3
    template_name = 'favorites_list.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user

            if user.role_id == UserRole.EMPLOYER:
                employer_profiles = EmployerProfile.objects.filter(user_id=user.pk)
                if employer_profiles:
                    profiler = employer_profiles.first()

                    employer_favorites = EmployerFavorites.objects.filter(
                        employer_profile=profiler).order_by('-created')

                    # Я ищу сотрудников и у меня есть вакансии. Мои вакансии.
                    vacancies = Vacancy.objects.filter(employer_profile=profiler)

                    # Вычисление оправлялось ли приглашение на резюме из избранного.
                    for favorit in employer_favorites:

                        favorit.has_relaton = False

                        # Отправлял ли я отклик на вакансии из избранного?
                        for vacancy in vacancies:
                            relations = Relations.objects.filter(cv=favorit.cv, vacancy=vacancy)
                            # Если relations, то отправлял.
                            if relations:
                                favorit.has_relaton = True
                                favorit.relations_id = relations.first().pk
                                break

                    return employer_favorites


    def get_context_data(self, **kwargs):
        context = super(FavoritesEmployerListView, self).get_context_data(**kwargs)
        context['title'] = "Избранное"
        context['heading'] = "Избранное"
        context['link'] = "/"
        context['heading_link'] = "На главную"
        context['is_employer'] = True

        if self.request.user.is_authenticated:
            user = self.request.user

            if user.role_id == UserRole.EMPLOYER:
                employer_profiles = EmployerProfile.objects.filter(user_id=user.pk)
                if employer_profiles:
                    profiler = employer_profiles.first()

                    # Я ищу сотрудников и у меня есть вакансии. Мои вакансии.
                    vacancies = Vacancy.objects.filter(employer_profile=profiler).exclude(status__status="NPB").\
                        exclude(status__status="RJC").exclude(is_active=False)

                    context['modal_header'] = 'Выбор вакансии'
                    context['modal_combo'] = vacancies
                    context['modal_combo_empty'] = 'Выберите вакансию'

        else:
            error_message = f'user is not authenticated'
            context['error_message'] = error_message
            print(error_message)

        return context
