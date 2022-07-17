from BestJob.settings import UserRole, RelationStatuses
from cvs.models import CV
from relations.models import RelationHistory, Relations, RelationStatus
from users.models import EmployerProfile, WorkerProfile
from vacancies.models import Vacancy


class CustomRelationModel:
    """Вспомогательный класс для формирования модели"""

    def __bool__(self):
        return any([self.__dict__[attr] for attr in self.__dict__.keys()])


def get_custom_relation_model(user, status_id, relation_id):
    '''
    Наполнение вспомогательного класса модели.
    :param status_id:
    :param relation_id:
    :return:
    '''
    custom_relation_model = CustomRelationModel()

    if (user.role_id == UserRole.EMPLOYER and (status_id == RelationStatuses.RESUME_NOT_VIEWED or status_id == RelationStatuses.RESUME_VIEWED or status_id == RelationStatuses.RESPONSE)) or \
        (user.role_id == UserRole.WORKER and (status_id == RelationStatuses.INVITATION_NOT_VIEWED or status_id == RelationStatuses.INVITATION_VIEWED or status_id == RelationStatuses.INVITATION)):
            custom_relation_model.button_text = 'Ответить'
            custom_relation_model.relation_id = relation_id

    return custom_relation_model


def set_modal_content(context, way_id):
    context['modal_header'] = 'Отправка ответа'
    context['modal_combo'] = RelationStatus.objects.filter(for_employer=True, for_worker=True)
    context['modal_combo_empty'] = 'Выберите статус ответа'
    context['modal_way_id'] = way_id


def set_detail_content(user, relation_id, context):
    global is_employer, is_worker

    # Работодатель.
    if user.role_id == UserRole.EMPLOYER:
        is_employer = True
        is_worker = False
    # Соискатель.
    elif user.role_id == UserRole.WORKER:
        is_employer = False
        is_worker = True

    relation_history = RelationHistory.objects.filter(relation_id=relation_id).order_by(
        '-status__status_priority')

    if relation_history:
        work_his = relation_history.first()
        relation_history.last_status = work_his.status.name
        relation_history.last_status_date = work_his.created
        relation_history.cv = work_his.relation.cv
        relation_history.vacancy = work_his.relation.vacancy
        relation_history.is_employer = is_employer
        relation_history.is_worker = is_worker

        custom_relation_model = get_custom_relation_model(user, work_his.status.pk, relation_id)

        if custom_relation_model:
            context['custom_relation_model'] = custom_relation_model

    context['relation_history'] = relation_history

    # Modal context
    set_modal_content(context, 1)


def set_watch_relation(user, relation_id):
    '''
    Установить статус просмотрено, если необходимо.
    :param user:
    :param relation_id:
    :return:
    '''
    relation_history = RelationHistory.objects.filter(relation_id=relation_id).order_by(
        '-status__status_priority')

    if relation_history:
        last_history = relation_history.first()

        new_relation_history = RelationHistory()
        new_relation_history.relation = Relations.objects.get(pk=relation_id)

        # Работодатель.
        if user.role_id == UserRole.EMPLOYER:
            if last_history.status.pk == RelationStatuses.RESUME_NOT_VIEWED:
                new_relation_history.status = RelationStatus.objects.get(pk=RelationStatuses.RESUME_VIEWED)
                new_relation_history.save()

        # Соискатель.
        elif user.role_id == UserRole.WORKER:
            if last_history.status.pk == RelationStatuses.INVITATION_NOT_VIEWED:
                new_relation_history.status = RelationStatus.objects.get(pk=RelationStatuses.INVITATION_VIEWED)
                new_relation_history.save()
