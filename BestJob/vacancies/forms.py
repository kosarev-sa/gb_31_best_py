from django import forms

from vacancies.models import Vacancy


class VacancyCreateForm(forms.ModelForm):
    """форма создание вакансии"""

    class Meta:
        model = Vacancy
        # fields = '__all__'
        exclude = ('employer_profile',)

    def __init__(self, *args, **kwargs):
        super(VacancyCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Backend разработчик'
        self.fields['city'].widget.attrs['placeholder'] = 'Москва'
        self.fields['description'].widget.attrs['placeholder'] = 'Описание вакансии'


class VacancyUpdateForm(forms.ModelForm):
    """форма просмотра\редактирования вакансии"""

    class Meta:
        model = Vacancy
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VacancyUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Backend разработчик'
        self.fields['city'].widget.attrs['placeholder'] = 'Москва'
        self.fields['description'].widget.attrs['placeholder'] = 'Описание вакансии'


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
