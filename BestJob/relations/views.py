from django.db.models import Max
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView

from BestJob.settings import UserRole
from cvs.models import CV
from users.models import EmployerProfile, WorkerProfile
from vacancies.models import Vacancy
from .models import Relations, RelationHistory, RelationStatus

WORKER_RS_ACCEPT_COMMENT = 'Встреча согласована'
WORKER_RS_CANCEL_COMMENT = 'Я не хочу у вас работать'
EMPLOYER_RS_ACCEPT_COMMENT = 'Встреча согласована'
EMPLOYER_RS_CANCEL_COMMENT = 'Мы свяжемся с вами позже'


class CustomRelationModel:

    def __bool__(self):
        return any([self.__dict__[attr] for attr in self.__dict__.keys()])


def get_custom_relation_model(user, status_id, relation_id):
    custom_relation_model = CustomRelationModel()

    # Работодатель.
    if user.role_id == UserRole.EMPLOYER:
        # Отклик
        if status_id == 5:
            custom_relation_model.accept_status_id = 6
            custom_relation_model.cancel_status_id = 3
            custom_relation_model.button_accept_text = 'Принять отклик'
            custom_relation_model.button_cancel_text = 'Отправить отказ'

    # Соискатель.
    elif user.role_id == UserRole.WORKER:
        # Приглашение
        if status_id == 4:
            custom_relation_model.accept_status_id = 6
            custom_relation_model.cancel_status_id = 3
            custom_relation_model.button_accept_text = 'Отправить отклик'
            custom_relation_model.button_cancel_text = 'Отправить отказ'

    if custom_relation_model:
        custom_relation_model.relation_id = relation_id

    return custom_relation_model


class LastListView(ListView):
    model = RelationStatus
    template_name = 'relation_last_list.html'

    def get_context_data(self, **kwargs):
        context = super(LastListView, self).get_context_data(**kwargs)
        context['title'] = "Отклики и приглашения"
        context['heading'] = "Отклики и приглашения"
        context['link'] = "/"
        context['heading_link'] = "На главную"
        return context

    def get(self, request, *args, **kwargs):
        super(LastListView, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        if request.user.is_authenticated:
            user = request.user

            relations = set()
            short_history_lists = list()

            # Работодатель.
            if user.role_id == UserRole.EMPLOYER:

                profile = EmployerProfile.objects.get(user_id=user.pk)
                if profile:
                    vacancies = Vacancy.objects.filter(employer_profile_id=profile.pk).order_by('-created_at')
                    if vacancies:
                        for vacancy in vacancies:
                            relation = Relations.objects.filter(vacancy_id=vacancy.pk).order_by('-created')
                            if relation:
                                for rel in relation:
                                    relations.add(rel)


            # Соискатель.
            elif user.role_id == UserRole.WORKER:

                profile = WorkerProfile.objects.get(user_id=user.pk)
                if profile:
                    cvs = CV.objects.filter(worker_profile_id=profile.pk).order_by('-date_create')
                    if cvs:
                        for cv in cvs:
                            relation = Relations.objects.filter(cv_id=cv.pk).order_by('-created')
                            if relation:
                                for rel in relation:
                                    relations.add(rel)

            for relation in relations:

                relation_history = RelationHistory.objects.filter(relation_id=relation.pk).order_by(
                    '-status__status_priority')

                if relation_history:
                    custom_relation_model = CustomRelationModel()
                    work_his = relation_history.first()
                    custom_relation_model.last_status = work_his.status.name
                    custom_relation_model.last_status_date = work_his.created
                    custom_relation_model.cv = work_his.relation.cv
                    custom_relation_model.vacancy = work_his.relation.vacancy
                    custom_relation_model.relation_id = work_his.relation.pk

                    status_info = get_custom_relation_model(user, work_his.status.pk, relation.pk)
                    if status_info:
                        custom_relation_model.status_info = status_info

                    short_history_lists.append(custom_relation_model)

            context['short_history_lists'] = short_history_lists

        else:
            error_message = f'user is not authenticated'
            context['error_message'] = error_message
            print(error_message)

        return self.render_to_response(context)


class RelationDetailView(TemplateView):
    model = RelationHistory
    template_name = 'relations_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RelationDetailView, self).get_context_data(**kwargs)
        context['title'] = "Отклики и приглашения"
        context['heading'] = "Отклики и приглашения"
        context['link'] = "/relations/list/"
        context['heading_link'] = "Назад"
        return context

    def get(self, request, *args, **kwargs):
        global relation_history
        super(RelationDetailView, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        if request.user.is_authenticated:
            user = request.user
            relation_id = kwargs.get('relation_id')

            relation_history = RelationHistory.objects.filter(relation_id=relation_id).order_by(
                '-status__status_priority')

            if relation_history:
                work_his = relation_history.first()
                relation_history.last_status = work_his.status.name
                relation_history.last_status_date = work_his.created
                relation_history.cv = work_his.relation.cv
                relation_history.vacancy = work_his.relation.vacancy

                custom_relation_model = get_custom_relation_model(user, work_his.status.pk, relation_id)

                if custom_relation_model:
                    context['custom_relation_model'] = custom_relation_model

            context['relation_history'] = relation_history

        else:
            error_message = f'user is not authenticated'
            context['error_message'] = error_message
            print(error_message)

        return self.render_to_response(context)


class RelationChangeStatusView(TemplateView):
    model = RelationHistory
    template_name = 'relations_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RelationChangeStatusView, self).get_context_data(**kwargs)
        context['title'] = "Отклики и приглашения"
        context['heading'] = "Отклики и приглашения"
        context['link'] = "/relations/list/"
        context['heading_link'] = "Назад"
        return context

    def get(self, request, *args, **kwargs):
        global relation_history
        super(RelationChangeStatusView, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        if request.user.is_authenticated:
            user = request.user
            relation_id = kwargs.get('relation_id')
            status_id = kwargs.get('status_id')

            new_rel_history = RelationHistory()
            new_rel_history.relation = Relations.objects.get(pk=relation_id)
            new_rel_history.status = RelationStatus.objects.get(pk=status_id)

            # Работодатель.
            if user.role_id == UserRole.EMPLOYER:
                if status_id < 6:
                    new_rel_history.comment = EMPLOYER_RS_CANCEL_COMMENT
                else:
                    new_rel_history.comment = EMPLOYER_RS_ACCEPT_COMMENT

            # Соискатель.
            elif user.role_id == UserRole.WORKER:
                if status_id < 6:
                    new_rel_history.comment = WORKER_RS_CANCEL_COMMENT
                else:
                    new_rel_history.comment = WORKER_RS_ACCEPT_COMMENT

            new_rel_history.save()

            relation_history = RelationHistory.objects.filter(relation_id=relation_id).order_by(
                '-status__status_priority')

            if relation_history:
                work_his = relation_history.first()
                relation_history.last_status = work_his.status.name
                relation_history.last_status_date = work_his.created
                relation_history.cv = work_his.relation.cv
                relation_history.vacancy = work_his.relation.vacancy

                custom_relation_model = get_custom_relation_model(user, work_his.status.pk, relation_id)

                if custom_relation_model:
                    context['custom_relation_model'] = custom_relation_model

            context['relation_history'] = relation_history

        else:
            error_message = f'user is not authenticated'
            context['error_message'] = error_message
            print(error_message)

        return self.render_to_response(context)


class RelationCreateView(CreateView):
    model = Relations
    success_url = reverse_lazy('relations:list')

    def post(self, request, *args, **kwargs):
        global status
        user = request.user
        if request.POST:
            form_data = request.POST
            magic_field = form_data.get('magic_field')
            relation_select_picker = form_data.get('relation_select_picker')
            transmittal_letter = form_data.get('transmittal_letter')

            if magic_field and relation_select_picker and transmittal_letter:
                magic_field = int(magic_field)
                relation_select_picker = int(relation_select_picker)

                new_relation = Relations()

                # Работодатель.
                if user.role_id == UserRole.EMPLOYER:
                    self.success_url = reverse_lazy('favorites:employer_list')
                    new_relation.vacancy = Vacancy.objects.get(pk=relation_select_picker)
                    new_relation.cv = CV.objects.get(pk=magic_field)
                    # Приглашение.
                    status = 4

                # Соискатель.
                elif user.role_id == UserRole.WORKER:
                    self.success_url = reverse_lazy('favorites:worker_list')
                    new_relation.cv = CV.objects.get(pk=relation_select_picker)
                    new_relation.vacancy = Vacancy.objects.get(pk=magic_field)
                    # Отклик.
                    status = 5

                new_relation.save()

                new_relation_history = RelationHistory()
                new_relation_history.relation = new_relation
                new_relation_history.status = RelationStatus.objects.get(pk=status)
                new_relation_history.comment = transmittal_letter
                new_relation_history.save()

        return redirect(self.success_url)

