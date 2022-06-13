from django import forms

from cvs.models import CV
from search.models import Category, Currency


class CVCreateForm(forms.ModelForm):
    """форма создание резюме"""

    class Meta:
        model = CV
        fields = ('post', 'speciality', 'salary', 'currency', 'education_level', 'moving')

    def __init__(self, *args, **kwargs):
        super(CVCreateForm, self).__init__(*args, **kwargs)
        self.fields['speciality'].widget.attrs['select'] = Category.objects.all()
        self.fields['post'].widget.attrs['placeholder'] = 'Желаемая должность'
        self.fields['salary'].widget.attrs['placeholder'] = 'Зарплата'
        # for field_name, field in self.fields.items():
        #     field.widget.attrs['class'] = 'form-control'
        # self.fields['data'].widget.attrs['placeholder'] = 'Введите data'


class CVUpdateForm(forms.ModelForm):
    """форма просмотра\редактирования резюме"""

    class Meta:
        model = CV
        fields = ('post', 'speciality', 'salary', 'currency', 'education_level', 'moving')

    def __init__(self, *args, **kwargs):
        super(CVUpdateForm, self).__init__(*args, **kwargs)
        # self.fields['data'].widget.attrs['placeholder'] = 'Введите data'


class CVDeleteForm(forms.ModelForm):
    """форма удаления резюме"""

    class Meta:
        model = CV
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CVDeleteForm, self).__init__(*args, **kwargs)
        # self.fields['data'].widget.attrs['placeholder'] = 'Введите data'


class CVDistributeForm(forms.ModelForm):
    """форма удаления резюме"""

    class Meta:
        model = CV
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CVDistributeForm, self).__init__(*args, **kwargs)
        # self.fields['data'].widget.attrs['placeholder'] = 'Введите data'
