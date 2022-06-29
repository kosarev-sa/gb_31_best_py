import hashlib
from random import random

from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm

from news.models import News
from users.models import WorkerProfile, EmployerProfile, ModeratorProfile, User, Role


class WorkerProfileForm(forms.ModelForm):
    """формы для профиля соискателя"""

    class Meta:
        model = WorkerProfile
        fields = ['name', 'image', 'city', 'phone_number', 'gender', 'birth_date', 'data']
        widgets = {
            'birth_date': DatePickerInput(
            options = {
                "format": "DD.MM.YYYY",
                "locale": "ru",
                "showClose": False,
                "showClear": True,
                "showTodayButton": True,
            }),
        }

    def __init__(self, *args, **kwargs):
        super(WorkerProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите ФИО'
        self.fields['city'].widget.attrs['placeholder'] = 'Введите город проживания'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Введите телефон для связи'
        self.fields['gender'].widget.attrs['placeholder'] = 'Введите Ваш пол'
        self.fields['birth_date'].widget.attrs['placeholder'] = 'Введите дату Вашего рождения'
        self.fields['data'].widget.attrs['placeholder'] = 'Введите пару слов о себе'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class EmployerProfileForm(forms.ModelForm):
    """формы для профиля работодателя"""

    class Meta:
        model = EmployerProfile
        # exclude = ['user']
        fields = ('name', 'image', 'city', 'data')

    def __init__(self, *args, **kwargs):
        super(EmployerProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите название компании'
        self.fields['city'].widget.attrs['placeholder'] = 'Введите город местонахождения'
        self.fields['data'].widget.attrs['placeholder'] = 'Введите описание компании'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ModeratorProfileForm(forms.ModelForm):
    """формы для профиля модератора"""

    class Meta:
        model = ModeratorProfile
        fields = ['image',]


class UserLoginForm(AuthenticationForm):
    """форма для логина"""

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'


class UserRegisterForm(UserCreationForm):
    """форма для регистрации"""

    class Meta:
        model = User
        fields = ('role', 'username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        
        # исключаем модератора быть выбранным при регистрации
        self.fields['role'].queryset = Role.objects.exclude(role_name='Модератор')
        self.fields['role'].widget.attrs.update({"class": "form-control"})
        self.fields['username'].widget.attrs.update({"class": "form-control", "placeholder": "Введите имя пользователя"})
        self.fields['email'].widget.attrs.update({"class": "form-control", "placeholder": "Введите адрес эл.почты"})
        self.fields['password1'].widget.attrs.update({"class": "form-control", "placeholder": "Введите пароль"})
        self.fields['password2'].widget.attrs.update({"class": "form-control", "placeholder": "Подтвердите пароль"})


    def save(self, commit=True):
        """переопределяем метод save для того, чтобы добавить ключ активации email"""
        user = super(UserRegisterForm, self).save()
        user.is_active = False
        salt = hashlib.sha256(str(random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha256((user.email + salt).encode('utf8')).hexdigest()
        user.save()
        return user


class PassResetForm(PasswordResetForm):
    """форма для востановления пароля (ввод email). нужна будет, чтобы поля под дизайн фронта переделать"""

    def __init__(self, *args, **kwargs):
        super(PassResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({"class": "form-control","placeholder": "email"})


class PassResetConfirmForm(SetPasswordForm):
    """форма для востановления пароля (ввод нового пароля). нужна будет, чтобы поля под дизайн фронта переделать"""

    def __init__(self, *args, **kwargs):
        super(PassResetConfirmForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({"placeholder": "пароль", "class":"form-control"})
        self.fields['new_password2'].widget.attrs.update({"placeholder": "подтверждение пароля", "class":"form-control"})

