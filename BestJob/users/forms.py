from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from news.models import News
from users.models import WorkerProfile, EmployerProfile, ModeratorProfile, User


class EmployeeProfileForm(forms.ModelForm):
    """формы для профиля соискателя"""

    class Meta:
        model = WorkerProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EmployeeProfileForm, self).__init__(*args, **kwargs)
        self.fields['data'].widget.attrs['placeholder'] = 'Введите data'


class EmployerProfileForm(forms.ModelForm):
    """формы для профиля работодателя"""

    class Meta:
        model = EmployerProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EmployerProfileForm, self).__init__(*args, **kwargs)
        self.fields['data'].widget.attrs['placeholder'] = 'Введите data'


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



class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"class": "form-control", "placeholder": "Введите имя пользователя"})
        self.fields['email'].widget.attrs.update({"class": "form-control", "placeholder": "Введите адрес эл.почты"})
        self.fields['password1'].widget.attrs.update({"class": "form-control", "placeholder": "Введите пароль"})
        self.fields['password2'].widget.attrs.update({"class": "form-control", "placeholder": "Подтвердите пароль"})
