from django.http import JsonResponse
from django.shortcuts import redirect

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView

from BestJob.settings import UserRole, RelationStatuses
from cvs.models import CV
from vacancies.models import Vacancy
from .content_helper import set_last_list_section_content, set_detail_content, set_watch_relation
from .models import Relations, RelationHistory, RelationStatus


class LastListView(ListView):
    """view отображения списка откликов и приглашений. Общий"""
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
            set_last_list_section_content(user, context)
        else:
            error_message = f'user is not authenticated'
            context['error_message'] = error_message
            print(error_message)

        return self.render_to_response(context)


class RelationDetailView(TemplateView):
    """view для показа детализации Откликов и приглашений"""
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

            set_watch_relation(user, relation_id)

            set_detail_content(user, relation_id, context)

        else:
            error_message = f'user is not authenticated'
            context['error_message'] = error_message
            print(error_message)

        return self.render_to_response(context)


class RelationCreateFromFavoritesView(CreateView):
    """view для создания Отклика или приглашения из модальной формы"""
    model = Relations
    success_url = reverse_lazy('relations:list')
    template_name = 'relation_last_list.html'

    def post(self, request, *args, **kwargs):
        global relation_link, status, unwatched_status
        user = request.user
        magic_field = kwargs.get('magic_id')
        relation_select_picker = kwargs.get('select_picker_id')
        transmittal_letter = kwargs.get('letter')

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
                status = RelationStatuses.INVITATION
                unwatched_status = RelationStatuses.INVITATION_NOT_VIEWED

            # Соискатель.
            elif user.role_id == UserRole.WORKER:
                self.success_url = reverse_lazy('favorites:worker_list')
                new_relation.cv = CV.objects.get(pk=relation_select_picker)
                new_relation.vacancy = Vacancy.objects.get(pk=magic_field)
                # Отклик.
                status = RelationStatuses.RESPONSE
                unwatched_status = RelationStatuses.RESUME_NOT_VIEWED

            new_relation.save()

            new_relation_history = RelationHistory()
            new_relation_history.relation = new_relation
            new_relation_history.status = RelationStatus.objects.get(pk=status)
            new_relation_history.comment = transmittal_letter
            new_relation_history.save()

            # Added unwatched relation history.
            new_unwatched_relation_history = RelationHistory()
            new_unwatched_relation_history.relation = new_relation
            new_unwatched_relation_history.status = RelationStatus.objects.get(pk=unwatched_status)
            new_unwatched_relation_history.comment = ''
            new_unwatched_relation_history.save()

            # Работодатель.
            if user.role_id == UserRole.EMPLOYER:
                relation_link = f'<a href="/relations/detail/{new_relation.pk}/"><h6 class="time">У вас есть взаимодействия по этому резюме</h6></a>'

            # Соискатель.
            elif user.role_id == UserRole.WORKER:
                relation_link = f'<a href="/relations/detail/{new_relation.pk}/"><h6 class="time">У вас есть взаимодействия по этой вакансии</h6></a>'

            return JsonResponse({'result': relation_link})

        return redirect(self.success_url)


class RelationCreateFromRelationView(CreateView):
    """view для создания Отклика или приглашения из модальной формы"""
    model = Relations
    success_url = reverse_lazy('relations:list')
    template_name = 'relation_last_list.html'

    def post(self, request, *args, **kwargs):
        user = request.user
        magic_field = kwargs.get('magic_id')
        relation_select_picker = kwargs.get('select_picker_id')
        transmittal_letter = kwargs.get('letter')

        if magic_field and relation_select_picker and transmittal_letter:
            magic_field = int(magic_field)
            relation_select_picker = int(relation_select_picker)

            relation = Relations.objects.get(pk=magic_field)

            set_watch_relation(user, relation.pk)

            relation_status = RelationStatus.objects.get(pk=relation_select_picker)

            new_relation_history = RelationHistory()
            new_relation_history.relation = relation
            new_relation_history.status = relation_status
            new_relation_history.comment = transmittal_letter
            new_relation_history.save()

            context = {}
            set_last_list_section_content(user, context)

            result = render_to_string(
                'inc_relation_last_list_section.html',
                context=context,
                request=request)

            return JsonResponse({'result': result})

        return redirect(self.success_url)


class RelationCreateFromRelationDetailView(CreateView):
    """view для создания Отклика или приглашения из модальной формы"""
    model = Relations
    success_url = reverse_lazy('relations:list')
    template_name = 'relation_last_list.html'

    def post(self, request, *args, **kwargs):
        user = request.user
        magic_field = kwargs.get('magic_id')
        relation_select_picker = kwargs.get('select_picker_id')
        transmittal_letter = kwargs.get('letter')

        if magic_field and relation_select_picker and transmittal_letter:
            magic_field = int(magic_field)
            relation_select_picker = int(relation_select_picker)

            relation = Relations.objects.get(pk=magic_field)

            set_watch_relation(user, relation.pk)

            relation_status = RelationStatus.objects.get(pk=relation_select_picker)

            new_relation_history = RelationHistory()
            new_relation_history.relation = relation
            new_relation_history.status = relation_status
            new_relation_history.comment = transmittal_letter
            new_relation_history.save()

            context = {}
            set_detail_content(user, magic_field, context)

            result = render_to_string(
                'inc_relation_detail_section.html',
                context=context,
                request=request)

            return JsonResponse({'result': result})

        return redirect(self.success_url)
