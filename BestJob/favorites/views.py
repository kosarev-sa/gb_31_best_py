from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView, DeleteView, ListView

from BestJob.settings import UserRole
from cvs.models import CV
from .models import EmployerFavorites, WorkerFavorites
from relations.models import Relations
from users.models import WorkerProfile, EmployerProfile
from vacancies.models import Vacancy


class FavoritesCreateView(CreateView):
    pass

class FavoritesDeleteView(DeleteView):
    pass

class FavoritesWorkerListView(ListView):
    template_name = 'favorites_list.html'
    queryset = WorkerFavorites.objects.all().none()

    def get_context_data(self, **kwargs):
        context = super(FavoritesWorkerListView, self).get_context_data(**kwargs)
        context['title'] = "Избранное"
        context['heading'] = "Избранное"
        context['link'] = "/"
        context['heading_link'] = "На главную"
        context['is_worker'] = True
        context['is_employer'] = False
        return context

    def get(self, request, *args, **kwargs):
        super(FavoritesWorkerListView, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        if request.user.is_authenticated:
            user = request.user

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
                        # Отправлял ли я отклик на вакансии из избранного?
                        for cv in cvs:
                            relations = Relations.objects.filter(cv=cv, vacancy=favorit.vacancy)
                            # Если relation, то отправлял.
                            if relations:
                                favorit.has_relaton = True
                                favorit.relations_id = relations.first().pk
                            else:
                                favorit.has_relaton = False

                    context['favorites_list'] = worker_favorites

        else:
            error_message = f'user is not authenticated'
            context['error_message'] = error_message
            print(error_message)

        return self.render_to_response(context)

class FavoritesEmployerListView(ListView):
    template_name = 'favorites_list.html'
    queryset = EmployerFavorites.objects.all().order_by('-created').none()
    context_object_name = 'favorites_list'

    def get_context_data(self, **kwargs):
        context = super(FavoritesEmployerListView, self).get_context_data(**kwargs)
        context['title'] = "Избранное"
        context['heading'] = "Избранное"
        context['link'] = "/"
        context['heading_link'] = "На главную"
        context['is_employer'] = True
        context['is_worker'] = False
        return context

    def get(self, request, *args, **kwargs):
        super(FavoritesEmployerListView, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        if request.user.is_authenticated:
            user = request.user

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

                        # Отправлял ли я отклик на вакансии из избранного?
                        for vacancy in vacancies:
                            relations = Relations.objects.filter(cv=favorit.cv, vacancy=vacancy)
                            # Если relations, то отправлял.
                            if relations:
                                favorit.has_relaton = True
                                favorit.relations_id = relations.first().pk
                            else:
                                favorit.has_relaton = False

                    context['favorites_list'] = employer_favorites
        else:
            error_message = f'user is not authenticated'
            context['error_message'] = error_message
            print(error_message)

        return self.render_to_response(context)

