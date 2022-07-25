from django import forms
from django.core.exceptions import ValidationError

from approvals.models import ApprovalStatus
from search.models import Category
from vacancies.models import Vacancy


class VacancyCreateForm(forms.ModelForm):
    """форма создание вакансии"""
    name = forms.CharField(label='Название вакансии', required=True)
    specialization = forms.ModelChoiceField(widget=forms.Select(),
                                            queryset=Category.objects.all().order_by('name'),
                                            label='Специализация', required=True)

    class Meta:
        model = Vacancy
        # fields = '__all__'
        exclude = ('employer_profile', 'status')

    def __init__(self, *args, **kwargs):
        super(VacancyCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Укажите название вакансии'
        self.fields['salary_from'].widget.attrs['placeholder'] = 'Укажите нижнюю границу заработной платы'
        self.fields['salary_to'].widget.attrs['placeholder'] = 'Укажите верхнюю границу заработной платы'
        self.fields['city'].widget.attrs['placeholder'] = 'Укажите город, например: Москва'
        self.fields['description'].widget.attrs['placeholder'] = 'Описание вакансии'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        data = self.cleaned_data['name']
        if len(data) > 50:
            raise ValidationError("Название должно быть не более 50 символов.")
        return data


class VacancyUpdateForm(forms.ModelForm):
    """форма просмотра\редактирования вакансии"""
    name = forms.CharField(label='Название вакансии', required=True)
    specialization = forms.ModelChoiceField(widget=forms.Select(),
                                            queryset=Category.objects.all().order_by('name'),
                                            label='Специализация', required=True)
    disabled_fields = ('moderators_comment',)

    class Meta:
        model = Vacancy
        exclude = ('employer_profile', 'status')

    def __init__(self, *args, **kwargs):
        super(VacancyUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs[
            'placeholder'] = 'Укажите название вакансии'
        self.fields['salary_from'].widget.attrs[
            'placeholder'] = 'Укажите нижнюю границу заработной платы'
        self.fields['salary_to'].widget.attrs[
            'placeholder'] = 'Укажите верхнюю границу заработной платы'
        self.fields['city'].widget.attrs[
            'placeholder'] = 'Укажите город, например: Москва'
        self.fields['description'].widget.attrs[
            'placeholder'] = 'Описание вакансии'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

            if field_name in ['specialization', 'currency']:
                field.widget.attrs['class'] = 'selectpicker'
                field.widget.attrs['data-size'] = '5'
                field.widget.attrs['data-container'] = 'body'

        for field in self.disabled_fields:
            self.fields[field].disabled = True

    def clean_name(self):
        data = self.cleaned_data['name']
        if len(data) > 50:
            raise ValidationError("Название должно быть не более 50 символов.")
        return data


class ModeratorVacancyUpdateForm(VacancyUpdateForm):
    """форма просмотра\редактирования вакансии"""
    name = forms.CharField(label='Название вакансии', required=False)
    disabled_fields = ('specialization', 'is_active', 'name', 'experience',
                       'description', 'city', 'description', 'salary_from',
                       'salary_to', 'currency', 'salary_on_hand')
    specialization = forms.ModelChoiceField(widget=forms.Select(),
                                            queryset=Category.objects.all().order_by('name'),
                                            label='Специализация', required=False)
    status = forms.ModelChoiceField(widget=forms.Select(),queryset=ApprovalStatus.objects.all().exclude(status='NPB'))

    class Meta:
        model = Vacancy
        exclude = ('employer_profile',)

    def __init__(self, *args, **kwargs):
        super(ModeratorVacancyUpdateForm, self).__init__(*args, **kwargs)
        # self.fields['status'].widget.attrs['class'] = 'selectpicker'
        for field in self.disabled_fields:
            self.fields[field].disabled = True

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'speciality':
                self.fields['status'].widget.attrs['data-size'] = '5'
                self.fields['status'].widget.attrs['data-container'] = 'body'


class VacancyDeleteForm(forms.ModelForm):
    """форма удаления вакансии"""

    class Meta:
        model = Vacancy
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VacancyDeleteForm, self).__init__(*args, **kwargs)


class VacancyDistributeForm(forms.ModelForm):
    """форма размещения вакансии"""

    class Meta:
        model = Vacancy
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VacancyDistributeForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Backend разработчик'
        self.fields['city'].widget.attrs['placeholder'] = 'Москва'
        self.fields['description'].widget.attrs['placeholder'] = 'Описание вакансии'
