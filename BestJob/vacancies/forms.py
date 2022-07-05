from django import forms

from approvals.models import ApprovalStatus
from search.models import Category
from vacancies.models import Vacancy
from cvs.models import ConnectVacancyCv


class VacancyCreateForm(forms.ModelForm):
    """форма создание вакансии"""

    class Meta:
        model = Vacancy
        # fields = '__all__'
        exclude = ('employer_profile', 'status')

    def __init__(self, *args, **kwargs):
        super(VacancyCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Backend разработчик'
        self.fields['city'].widget.attrs['placeholder'] = 'Москва'
        self.fields['description'].widget.attrs['placeholder'] = 'Описание вакансии'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class VacancyUpdateForm(forms.ModelForm):
    """форма просмотра\редактирования вакансии"""
    specialization = forms.ModelChoiceField(widget=forms.Select(), queryset=Category.objects.all().order_by('name'),
                                            required=False)
    disabled_fields = ('moderators_comment',)

    class Meta:
        model = Vacancy
        exclude = ('employer_profile', 'status')

    def __init__(self, *args, **kwargs):
        super(VacancyUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Backend разработчик'
        self.fields['city'].widget.attrs['placeholder'] = 'Москва'
        self.fields['description'].widget.attrs['placeholder'] = 'Описание вакансии'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

            if field_name in ['specialization', 'currency']:
                field.widget.attrs['class'] = 'selectpicker'
                field.widget.attrs['data-size'] = '5'
                field.widget.attrs['data-container'] = 'body'

        for field in self.disabled_fields:
            self.fields[field].disabled = True


class ModeratorVacancyUpdateForm(VacancyUpdateForm):
    """форма просмотра\редактирования вакансии"""
    disabled_fields = ('specialization', 'is_active', 'name', 'experience',
                       'description', 'city', 'description', 'salary_from',
                       'salary_to', 'currency', 'salary_on_hand',)
    status = forms.ModelChoiceField(widget=forms.Select(),
                                    queryset=ApprovalStatus.objects.exclude(status='NPV'),  # почему-то exclude не отрабатываеит
                                    required=False)

    class Meta:
        model = Vacancy
        exclude = ('employer_profile',)

    def __init__(self, *args, **kwargs):
        super(ModeratorVacancyUpdateForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs['class'] = 'selectpicker'
        for field in self.disabled_fields:
            self.fields[field].disabled = True


class VacancyDeleteForm(forms.ModelForm):
    """форма удаления вакансии"""

    class Meta:
        model = Vacancy
        fields = '__all__'


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


class VacancyResponseForm(forms.ModelForm):
    """форма изменения отклика на вакансию"""

    class Meta:
        model = ConnectVacancyCv
        exclude = ('cv', 'vacancy', 'status_worker', 'created_at', 'initiator')
