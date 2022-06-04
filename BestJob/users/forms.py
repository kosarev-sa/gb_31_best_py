from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from news.models import News
from users.models import WorkerProfile, EmployerProfile, ModeratorProfile, User


class WorkerProfileForm(forms.ModelForm):
    """формы для профиля соискателя"""

    class Meta:
        model = WorkerProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(WorkerProfileForm, self).__init__(*args, **kwargs)
        self.fields['data'].widget.attrs['placeholder'] = 'Введите data'


class EmployerProfileForm(forms.ModelForm):
    """формы для профиля работодателя"""

    class Meta:
        model = EmployerProfile
        exclude = ('user', 'date_create', 'is_active', 'status', )

    def __init__(self, *args, **kwargs):
        super(EmployerProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите название компании'
        self.fields['city'].widget.attrs['placeholder'] = 'Введите город местонахождения'
        self.fields['data'].widget.attrs['placeholder'] = 'Введите описание компании'


class ModeratorProfileForm(forms.ModelForm):
    """формы для профиля модератора"""

    class Meta:
        model = ModeratorProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ModeratorProfileForm, self).__init__(*args, **kwargs)
        self.fields['data'].widget.attrs['placeholder'] = 'Введите data'


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите адрес эл.почты'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтвердите пароль'
