# Create your views here.
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string

from BestJob.mixin import BaseClassContextMixin, UserDispatchMixin

from django.contrib import auth, messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, FormView, TemplateView, ListView, DetailView

from BestJob import settings
from BestJob.settings import UserRole
from approvals.models import ApprovalStatus
from news.models import News
from search.models import Category
from users.forms import WorkerProfileForm, EmployerProfileForm, ModeratorProfileForm, UserLoginForm, UserRegisterForm, \
    PassResetForm, PassResetConfirmForm, ModeratorCompanyUpdateForm

from users.models import WorkerProfile, EmployerProfile, ModeratorProfile, User


class WorkerProfileView(UpdateView):
    """view для профиля соискателя"""
    model = WorkerProfile
    template_name = 'worker_profile.html'
    form_class = WorkerProfileForm
    success_url = reverse_lazy('users:worker_profile')
    # title = 'BestJob | Профайл соискателя'

    def get_object(self, queryset=None):
        user_id = self.kwargs['pk']
        worker_profile = WorkerProfile.objects.filter(user_id=user_id)

        if worker_profile:
            return worker_profile.first()
        else:
            worker_profile = WorkerProfile()
            worker_profile.user = User.objects.get(pk=user_id)
            return worker_profile

    def get_context_data(self, **kwargs):
        context = super(WorkerProfileView, self).get_context_data(**kwargs)

        context['title'] = "Профиль соискателя"
        context['heading'] = "Профиль соискателя"
        # context['link'] = "/cvs/all/"
        # context['heading_link'] = "Список резюме"
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(data=request.POST, files=request.FILES, instance=self.object)
        user_id = self.kwargs['pk']

        workerProfile = WorkerProfile.objects.filter(user_id=user_id)

        if workerProfile:
            workerProfile = workerProfile.first()
            form.instance.pk = workerProfile.id
            form.instance.user_id = workerProfile.user.id
            form.instance.user = workerProfile.user

            if form.instance.image.closed:
                form.instance.image = workerProfile.image

        else:
            form.instance.user_id = user_id
            form.instance.user = User.objects.get(pk=user_id)

        if form.is_valid():
            if not form.has_changed():
                messages.error(request, 'Для сохранения измените хотя бы одно поле!')
                return self.form_invalid(form)
            form.save()
            messages.success(request, 'Профиль успешно отредактирован!')
            return redirect(reverse("users:worker_profile", args=(user_id,)))
        else:
            print(form.errors)
            messages.error(request, 'Проверьте правильность заполнения Профиля!')
        return self.form_invalid(form)


class EmployersProfileView(ListView, BaseClassContextMixin):
    """view для просмотра работодателей"""
    model = EmployerProfile
    template_name = 'employers.html'
    # paginate_by = 3
    title = 'BestJob | Работодатели'

    def get_context_data(self, **kwargs):
        context = super(EmployersProfileView, self).get_context_data(**kwargs)
        context.update({
            'employers': EmployerProfile.objects.all(),
        })
        return context


class EmployerDetailView(DetailView, BaseClassContextMixin):
    """view для просмотра выбранного работодателя"""
    model = EmployerProfile
    template_name = 'employers_detail.html'
    title = 'Карточка компании'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EmployerDetailView, self).get_context_data(**kwargs)
        comp_id = self.kwargs['pk']
        company = EmployerProfile.objects.get(id=comp_id)
        context['object'] = company
        context['title'] = company.name
        context['heading'] = 'Карточка работодателя'
        context['is_moderating'] = False
        return context


class ModeratorCompanyUpdate(UpdateView):
    """view модерации выбранного работодателя"""
    model = EmployerProfile
    template_name = 'employers_detail.html'
    form_class = ModeratorCompanyUpdateForm
    success_url = reverse_lazy('users:moderator_companies_list')

    def get(self, request, *args, **kwargs):
        super(ModeratorCompanyUpdate, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        comp_id = self.kwargs['pk']
        company = EmployerProfile.objects.get(id=comp_id)
        context['object'] = company
        # context['title'] = company.name
        context['is_moderating'] = True

        context['title'] = "Модерация компании"
        context['heading'] = "Модерация компании"
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        comp_id = self.kwargs['pk']
        if form.is_valid():
            EmployerProfile.objects.filter(pk=comp_id).update(status=form.instance.status,
                                               moderators_comment=form.instance.moderators_comment)
        else:
            print(form.errors)
        return redirect(self.success_url)


class EmployerProfileView(UpdateView):
    """view для профиля работодателя"""
    model = EmployerProfile
    template_name = 'employer_profile.html'
    form_class = EmployerProfileForm
    success_url = reverse_lazy('users:employer_profile')
    title = 'BestJob | Профайл работодателя'

    def get_object(self, queryset=None):
        pk = self.kwargs['pk']

        employer_profile = EmployerProfile.objects.filter(user_id=pk)

        if employer_profile:
            return employer_profile.first()
        else:
            employer_profile = EmployerProfile.objects.filter(pk=pk)
            if employer_profile:
                return employer_profile.first()
            else:
                employer_profile = EmployerProfile()
                employer_profile.user = User.objects.get(pk=pk)
                return employer_profile

    def get_context_data(self, **kwargs):
        context = super(EmployerProfileView, self).get_context_data(**kwargs)

        context['title'] = "Профиль работодателя"
        context['heading'] = "Профиль работодателя"
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # form = self.form_class(data=request.POST, files=request.FILES)
        form = self.form_class(request.POST, instance=self.object, files=request.FILES)
        user_id = self.kwargs['pk']

        emploerProfile = EmployerProfile.objects.filter(user_id=user_id)

        if emploerProfile:
            emploerProfile = emploerProfile.first()
            form.instance.pk = emploerProfile.id
            form.instance.user_id = emploerProfile.user.id
            form.instance.user = emploerProfile.user
            form.instance.data = emploerProfile.data
            form.instance.date_create = emploerProfile.date_create

            if form.instance.image.closed:
                form.instance.image = emploerProfile.image
        else:
            form.instance.user_id = user_id
            form.instance.user = User.objects.get(pk=user_id)

        if form.is_valid():
            if not form.has_changed():
                messages.error(request, 'Для сохранения измените хотя бы одно поле!')
                return self.form_invalid(form)
            form.save()
            messages.success(request, 'Профиль успешно отредактирован!')
            return redirect(reverse("users:employer_profile", args=(user_id,)))
        else:
            print(form.errors)
            messages.error(request, 'Проверьте правильность заполнения Профиля!')
        return self.form_invalid(form)


class ModeratorProfileView(UpdateView):
    """view для профиля модератора"""
    model = ModeratorProfile
    template_name = 'moderator_profile.html'
    form_class = ModeratorProfileForm
    success_url = reverse_lazy('users:moderator_profile')
    title = 'BestJob | Профайл модератора'

    def get_object(self, queryset=None):
        user_id = self.kwargs['pk']
        moderator_profile = ModeratorProfile.objects.filter(user_id=user_id)

        if moderator_profile:
            return moderator_profile.first()
        else:
            moderator_profile = ModeratorProfile()
            moderator_profile.user = User.objects.get(pk=user_id)
            return moderator_profile

    def get_context_data(self, **kwargs):
        context = super(ModeratorProfileView, self).get_context_data(**kwargs)

        context['title'] = "Профиль модератора"
        context['heading'] = "Профиль модератора"
        context['link'] = "/news/all/"
        context['heading_link'] = "Список новостей"
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.form_class(data=request.POST, files=request.FILES, instance=self.object)
        user_id = self.kwargs['pk']
        moderatorProfile = ModeratorProfile.objects.filter(user_id=user_id)

        if moderatorProfile:
            moderatorProfile = moderatorProfile.first()
            form.instance.pk = moderatorProfile.id
            form.instance.user_id = moderatorProfile.user.id
            form.instance.user = moderatorProfile.user
            form.instance.date_create = moderatorProfile.date_create

            if form.instance.image.closed:
                form.instance.image = moderatorProfile.image

        else:
            form.instance.user_id = user_id
            form.instance.user = User.objects.get(pk=user_id)

        if form.is_valid():
            if not form.has_changed():
                messages.error(request, 'Для сохранения измените хотя бы одно поле!')
                return self.form_invalid(form)
            form.save()
            messages.success(request, 'Профиль успешно отредактирован!')
            return redirect(reverse("users:moderator_profile", args=(user_id,)))
        else:
            print(form.errors)
            messages.error(request, 'Проверьте правильность заполнения Профиля!')
        return self.form_invalid(form)


class UserLoginView(LoginView):
    """view для логина"""
    template_name = 'user_login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(UserLoginView, self).get_context_data()
        context['title'] = 'Авторизация'
        context['link'] = '/'
        context['heading_link'] = 'На главную'
        return context


class UserRegisterView(FormView):
    """view для регистрации"""
    model = User
    template_name = 'user_register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:email_verify')
    unsuccess_url = reverse_lazy('users:registration')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserRegisterView, self).get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['link'] = '/'
        context['heading_link'] = 'На главную'
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """метод сохранения нового юзера. изначально он не активен, нужно подтвердить email"""
        global user, employer_profile, worker_profile
        form = self.form_class(data=request.POST)
        sid = transaction.savepoint()
        if form.is_valid():
            try:
                # сохраняем нового юзера
                user = form.save()
                # отправляем email с подтверждением почты
                self.send_verify_link(user)
                # создаем профиль в зависимости от роли
                if user.role_id == UserRole.EMPLOYER:
                    employer_profile = EmployerProfile(user_id=user.pk)
                    employer_profile.save()
                elif user.role_id == UserRole.WORKER:
                    worker_profile = WorkerProfile(user_id=user.pk)
                    worker_profile.save()

                transaction.savepoint_commit(sid)

                messages.success(request, 'Профиль успешно зарегистрирован!')
                return redirect(self.success_url)
            except Exception as e:
                transaction.savepoint_rollback(sid)
                messages.error(request, f'500 внутренняя ошибка сервера\n{e}')
                return self.form_invalid(form)
        else:
            print(form.errors)
            messages.error(request, 'Проверьте правильность заполнения формы!')
        return self.form_invalid(form)

    def send_verify_link(self, user):
        """отправляем письмо с сылкой на активацией профиля"""
        verify_link = reverse('users:verify', args=[user.username, user.email, user.activation_key])
        subject = f'Для активации учетной записи {user.username} пройдите по ссылке'
        message = f'Для подтверждения учетной записи {user.username} на портале \n {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def verify(self, username, email, activation_key):
        """проверяем, что ключ в ссылке совпадает с ключем в бд и не прошло 48 часов"""
        user = User.objects.get(email=email, username=username)
        if user and user.activation_key == activation_key and not user.is_activation_key_expired():
            user.activation_key = ''
            user.activation_key_created = None
            user.is_active = True
            user.save()
        auth.login(self, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect(reverse_lazy('users:verify_status'))


class UserLogoutView(LogoutView):
    """view для выхода из-под учетки"""
    template_name = 'index.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserLogoutView, self).get_context_data(**kwargs)
        news_list = News.objects.filter(is_active=True).order_by('-created')

        if news_list:
            if len(news_list) >= 3:
                #  Берём top 3.
                context['news_list'] = news_list[:3]

        context['categories'] = Category.objects.all().order_by('name')
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.success_url)

        return super(UserLogoutView, self).get(request, *args, **kwargs)


class UserEmailVarifyView(TemplateView):
    """view вывода времени на активацию учетки"""
    template_name = 'user_email_confirmation.html'

    def get_context_data(self, **kwargs):
        context = super(UserEmailVarifyView, self).get_context_data()
        # передаем в контексте из настроек, сколько есть времени на активацию профиля
        context['verify_time'] = settings.USER_EMAIL_KEY_LIFETIME
        context['title'] = 'Подтверждение E-mail'
        context['link'] = '/'
        context['heading_link'] = 'На главную'
        return context


class UserVarifyStatusView(TemplateView):
    """view для результата активации профиля"""
    template_name = 'user_verify.html'

    def get_context_data(self, **kwargs):
        context = super(UserVarifyStatusView, self).get_context_data()
        context['title'] = 'Активация пользователя'
        context['link'] = '/'
        context['heading_link'] = 'На главную'
        return context


class PassResetView(PasswordResetView):
    """view сброса пароля по email"""
    email_template_name = 'password_reset_email.html'
    template_name = 'password_reset.html'
    success_url = reverse_lazy("users:password_reset_done")
    form_class = PassResetForm

    def get_context_data(self, **kwargs):
        context = super(PassResetView, self).get_context_data()
        context['title'] = 'Сброс пароля'
        context['link'] = '/'
        context['heading_link'] = 'На главную'
        return context


class PassResetDoneView(PasswordResetDoneView):
    """view о том, что пароль сброшен"""
    template_name = 'password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super(PassResetDoneView, self).get_context_data()
        context['title'] = 'Cброс пароля выполнен'
        return context


class PassResetConfirmView(PasswordResetConfirmView):
    """view для ввода нового пароля"""

    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy("users:password_reset_complete")
    form_class = PassResetConfirmForm

    def get_context_data(self, **kwargs):
        context = super(PassResetConfirmView, self).get_context_data()
        context['title'] = 'Ввод нового пароля'
        return context


class PassResetCompletedView(PasswordResetCompleteView):
    """view что новый пароль сохранен"""
    template_name = 'password_reset_completed.html'

    def get_context_data(self, **kwargs):
        context = super(PassResetCompletedView, self).get_context_data()
        context['title'] = 'Новый пароль сохранен'
        context['link'] = '/'
        context['heading_link'] = 'На главную'
        return context


class ModerationAwaiting(TemplateView):
    """view ожидают модерации"""
    template_name = 'moderation_awaiting.html'
    success_url = reverse_lazy("users:moderation_awaiting")
    title = 'BestJob | Модерация'


class ModeratorCompaniesList(TemplateView):
    """view просмотра вакансий модератором"""
    template_name = 'moderator_company_list.html'

    def get(self, request, *args, **kwargs):
        super(ModeratorCompaniesList, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        context['companies_list'] = EmployerProfile.objects.filter(status__status="PUB")
        # EmployerProfile.objects.exclude(status__status="NPB")
        context['title'] = 'Модерация компаний'
        context['heading'] = 'Модерация компаний'
        return self.render_to_response(context)


def edit_comp_list(request, stat):
    """Обновление списка компаний соглано статусу на странице список компаний у модератора"""
    companies_list = EmployerProfile.objects.exclude(status__status="NPB")

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # вместо отмершего if request.is_ajax()
        if stat == 'frv':
            companies_list = EmployerProfile.objects.filter(status__status="FRV")
        elif stat == 'all':
            companies_list = EmployerProfile.objects.exclude(status__status="NPB")
        elif stat == 'pub':
            companies_list = EmployerProfile.objects.filter(status__status="PUB")
        elif stat == 'rjc':
            companies_list = EmployerProfile.objects.filter(status__status="RJC")
        elif stat == 'apv':
            companies_list = EmployerProfile.objects.filter(status__status="APV")
        else:
            companies_list = EmployerProfile.objects.exclude(status__status="NPB")
    context = {'companies_list': companies_list}
    result = render_to_string('companies_list.html', context)

    return JsonResponse({'result': result})


def set_public_status(request, pk):
    empl = get_object_or_404(EmployerProfile, pk=pk)
    empl.status = ApprovalStatus.objects.get(status='PUB')
    empl.save()
    return HttpResponseRedirect(reverse('users:employer_profile', args=(pk,)))
