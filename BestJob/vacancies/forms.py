from django import forms

from vacancies.models import Vacancy


class VacancyCreateForm(forms.ModelForm):
    """форма создание вакансии"""

    class Meta:
        model = Vacancy
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VacancyCreateForm, self).__init__(*args, **kwargs)
        self.fields['data'].widget.attrs['placeholder'] = 'Введите data'


class VacancyUpdateForm(forms.ModelForm):
    """форма просмотра\редактирования вакансии"""

    class Meta:
        model = Vacancy
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VacancyUpdateForm, self).__init__(*args, **kwargs)
        self.fields['data'].widget.attrs['placeholder'] = 'Введите data'


class VacancyDeleteForm(forms.ModelForm):
    """форма удаления вакансии"""

    class Meta:
        model = Vacancy
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VacancyDeleteForm, self).__init__(*args, **kwargs)
        self.fields['data'].widget.attrs['placeholder'] = 'Введите data'


class VacancyDistributeForm(forms.ModelForm):
    """форма удаления вакансии"""

    class Meta:
        model = Vacancy
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VacancyDistributeForm, self).__init__(*args, **kwargs)
        self.fields['data'].widget.attrs['placeholder'] = 'Введите data'
