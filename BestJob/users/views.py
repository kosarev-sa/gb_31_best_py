# Create your views here.
from django.http import HttpResponseRedirect

from BestJob.mixin import BaseClassContextMixin, UserDispatchMixin

from django.contrib import auth
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, FormView, TemplateView, ListView, DetailView

from BestJob import settings
from news.models import News
from search.models import Category
from users.forms import WorkerProfileForm, EmployerProfileForm, ModeratorProfileForm, UserLoginForm, UserRegisterForm, \
    PassResetForm, PassResetConfirmForm

from users.models import WorkerProfile, EmployerProfile, ModeratorProfile, User


class WorkerProfileView(UpdateView):
    """view для профиля соискателя"""
    model = WorkerProfile
    template_name = 'worker_profile.html'
    form_class = WorkerProfileForm
    success_url = reverse_lazy('users:worker_profile')
    title = 'BestJob | Профайл соискателя'

    def get_object(self, queryset=None):
        user_id = self.kwargs['pk']
        worker_profile = WorkerProfile.objects.filter(user_id=user_id)

        if worker_profile:
            return worker_profile.first()
        else:
            worker_profile = WorkerProfile()
            worker_profile.user = User.objects.get(pk=user_id)
            return worker_profile


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(data=request.POST, files=request.FILES)
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

        form.save()
        return redirect(reverse("users:worker_profile", args=(user_id,)))


class EmployersProfileView(ListView, BaseClassContextMixin):
    """view для просмотра работодателей"""
    model = EmployerProfile
    template_name = 'employers.html'
    # paginate_by = 3
    title = 'BestJob | Работодатели'

    def get_context_data(self, **kwargs):
        context = super(EmployerProfileView, self).get_context_data(**kwargs)
        context.update({
            'employers': EmployerProfile.objects.all(),
        })
        return context


class EmployerDetailView(DetailView, BaseClassContextMixin):
    """view для просмотра выбранного работодателя"""
    model = EmployerProfile
    template_name = 'employers_detail.html'
    title = 'BestJob | Работодатель'

#
# class EmployerProfileFormView(UpdateView, BaseClassContextMixin, UserDispatchMixin):
#     """view для профиля работодателя"""
#     model = EmployerProfile
#     form_class = EmployerProfileForm
#     template_name = 'employer_profile.html'
#     success_url = reverse_lazy('users:employer_profile')
#     title = 'BestJob | Профайл работодателя'
#
#     # def get_object(self, queryset=None):
#     #     return get_object_or_404(User, pk=self.request.employer_profile.pk)


class EmployerProfileView(UpdateView):
    """view для профиля работодателя"""
    model = EmployerProfile
    template_name = 'employer_profile.html'
    form_class = EmployerProfileForm
    success_url = reverse_lazy('users:employer_profile')
    title = 'BestJob | Профайл работодателя'

    def get_object(self, queryset=None):
        user_id = self.kwargs['pk']
        employer_profile = EmployerProfile.objects.filter(user_id=user_id)

        if employer_profile:
            return employer_profile.first()
        else:
            employer_profile = EmployerProfile()
            employer_profile.user = User.objects.get(pk=user_id)
            return employer_profile
        

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(data=request.POST, files=request.FILES)
        user_id = self.kwargs['pk']

        emploerProfile = EmployerProfile.objects.filter(user_id=user_id)

        if emploerProfile:
            emploerProfile = emploerProfile.first()
            form.instance.pk = emploerProfile.id
            form.instance.user_id = emploerProfile.user.id
            form.instance.user = emploerProfile.user
            form.instance.date_create = emploerProfile.date_create

            if form.instance.image.closed:
                form.instance.image = emploerProfile.image
        else:
            form.instance.user_id = user_id
            form.instance.user = User.objects.get(pk=user_id)

        form.save()
        return redirect(reverse("users:employer_profile", args=(user_id,)))


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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.form_class(data=request.POST, files=request.FILES)
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

        form.save()
        return redirect(reverse("users:moderator_profile", args=(user_id,)))


class UserLoginView(LoginView):
    """view для логина"""
    template_name = 'user_login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(UserLoginView, self).get_context_data()
        return context


class UserRegisterView(FormView):
    """view для регистрации"""
    model = User
    template_name = 'user_register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:email_verify')
    unsuccess_url = reverse_lazy('users:registration')

    def post(self, request, *args, **kwargs):
        """метод сохранения нового юзера. изначально он не активен, нужно подтвердить email"""
        form = self.form_class(data=request.POST)
        if form.is_valid():
            # сохраняем нового юзера
            user = form.save()
            # отправляем email с подтверждением почты
            self.send_verify_link(user)
            # создаем профиль в зависимости от роли
            if user.role_id == 2:
                employer_profile = EmployerProfile(user_id=user.pk)
                employer_profile.save()
            elif user.role_id == 3:
                worker_profile = WorkerProfile(user_id=user.pk)
                worker_profile.save()

            return redirect(self.success_url)
        else:
            print(form.errors)
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserLogoutView, self).get_context_data(**kwargs)
        news_list = News.objects.filter(is_active=True).order_by('-created')

        if news_list:
            if len(news_list) >= 3:
                #  Берём top 3.
                context['news_list'] = news_list[:3]

        context['categories'] = Category.objects.all().order_by('name')
        return context


class UserEmailVarifyView(TemplateView):
    """view вывода времени на активацию учетки"""
    template_name = 'user_email_confirmation.html'

    def get_context_data(self, **kwargs):
        context = super(UserEmailVarifyView, self).get_context_data()
        # передаем в контексте из настроек, сколько есть времени на активацию профиля
        context['verify_time'] = settings.USER_EMAIL_KEY_LIFETIME
        return context


class UserVarifyStatusView(TemplateView):
    """view для результата активации профиля"""
    template_name = 'user_verify.html'


class PassResetView(PasswordResetView):
    """view сброса пароля по email"""
    email_template_name = 'password_reset_email.html'
    template_name = 'password_reset.html'
    success_url = reverse_lazy("users:password_reset_done")
    form_class = PassResetForm


class PassResetDoneView(PasswordResetDoneView):
    """view о том, что пароль сброшен"""
    template_name = 'password_reset_done.html'


class PassResetConfirmView(PasswordResetConfirmView):
    """view для ввода нового пароля"""

    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy("users:password_reset_complete")
    form_class = PassResetConfirmForm


class PassResetCompletedView(PasswordResetCompleteView):
    """view что новый пароль сохранен"""
    template_name = 'password_reset_completed.html'


class ModerationAwaiting(TemplateView):
    """view ожидают модерации"""
    template_name = 'moderation_awaiting.html'
    success_url = reverse_lazy("users:moderation_awaiting")
    title = 'BestJob | Модерация'
