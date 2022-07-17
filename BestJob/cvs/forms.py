from django import forms
import time
import datetime

from django.core.exceptions import ValidationError

from approvals.models import ApprovalStatus
from cvs.models import CV, Experience, Education, LanguagesSpoken
from search.models import Category, Currency, Languages, LanguageLevels

now = datetime.datetime.now()


class CVCreateForm(forms.ModelForm):
    """форма создание резюме"""
    speciality = forms.ModelChoiceField(widget=forms.Select(),
                                        queryset=Category.objects.all().order_by('name'),
                                        required=True, label='Специализация')
    post = forms.CharField(widget=forms.TextInput, required=True, label='Должность')
    skills = forms.CharField(widget=forms.TextInput, required=False)
    about = forms.CharField(widget=forms.Textarea, required=False)
    salary = forms.DecimalField(label='Зарплата', required=False)

    class Meta:
        model = CV
        fields = ('post', 'speciality', 'salary', 'currency', 'education_level', 'moving', 'skills', 'about')

    def __init__(self, *args, **kwargs):
        super(CVCreateForm, self).__init__(*args, **kwargs)
        self.fields['speciality'].widget.attrs['select'] = Category.objects.all()
        self.fields['post'].widget.attrs['placeholder'] = 'Желаемая должность'
        self.fields['salary'].widget.attrs['placeholder'] = 'Зарплата'
        self.fields['skills'].widget.attrs['placeholder'] = 'Укажите Ваши основные навыки, разделяя их запятыми. Например: Python, Django, Flask, DRF'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

            if field_name in ['speciality', 'currency', 'education_level', 'moving']:
                field.widget.attrs['class'] = 'selectpicker'
                field.widget.attrs['data-size'] = '5'
                field.widget.attrs['data-container'] = 'body'

        # self.fields['about'].widget.attrs['class'] = "tinymce"

    def clean_post(self):
        data = self.cleaned_data['post']
        if len(data) > 30:
            raise ValidationError("Сократите название должности.")
        return data


class CVUpdateForm(forms.ModelForm):
    """форма просмотра\редактирования резюме"""
    disabled_fields = ('moderators_comment',)
    speciality = forms.ModelChoiceField(widget=forms.Select(),
                                        queryset=Category.objects.all().order_by('name'),
                                        required=True, label='Специализация')
    post = forms.CharField(widget=forms.TextInput, required=True, label='Должность')
    skills = forms.CharField(widget=forms.TextInput, required=False)
    about = forms.CharField(widget=forms.Textarea, required=False)
    salary = forms.DecimalField(label='Зарплата', required=False)

    class Meta:
        model = CV
        fields = ('post', 'speciality', 'salary', 'currency', 'education_level', 'moving', 'skills', 'about', 'moderators_comment')

    def __init__(self, *args, **kwargs):
        super(CVUpdateForm, self).__init__(*args, **kwargs)
        self.fields['speciality'].widget.attrs['select'] = Category.objects.all()
        self.fields['post'].widget.attrs['placeholder'] = 'Желаемая должность'
        self.fields['salary'].widget.attrs['placeholder'] = 'Зарплата'
        self.fields['skills'].widget.attrs[
            'placeholder'] = 'Укажите Ваши основные навыки, разделяя их запятыми. Например: Python, Django, Flask, DRF'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

            if field_name in ['speciality', 'currency', 'education_level', 'moving']:
                field.widget.attrs['class'] = 'selectpicker'
                field.widget.attrs['data-size'] = '5'
                field.widget.attrs['data-container'] = 'body'

        for field in self.disabled_fields:
            self.fields[field].disabled = True

        # self.fields['about'].widget.attrs['class'] = "tinymce"

    def clean_post(self):
        data = self.cleaned_data['post']
        if len(data) > 30:
            raise ValidationError("Сократите название должности.")
        return data


class ModeratorCVUpdateForm(CVUpdateForm):
    """форма просмотра\редактирования резюме"""
    speciality = forms.ModelChoiceField(widget=forms.Select(),
                                        queryset=Category.objects.all().order_by('name'),
                                        required=False, label='Специализация')
    post = forms.CharField(widget=forms.TextInput, required=False, label='Должность')
    status = forms.ModelChoiceField(widget=forms.Select(),queryset=ApprovalStatus.objects.all().exclude(status='NPB'))

    disabled_fields = ('is_active', 'post', 'skills', 'education_level', 'moving', 'salary', 'currency', 'speciality')

    class Meta:
        model = CV
        exclude = ('worker_profile',)

    def __init__(self, *args, **kwargs):
        super(ModeratorCVUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'speciality':
                self.fields['status'].widget.attrs['data-size'] = '5'
                self.fields['status'].widget.attrs['data-container'] = 'body'

        for field in self.disabled_fields:
            self.fields[field].disabled = True



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


class ExperienceCreateForm(forms.ModelForm):
    """форма создания опыта работы"""
    responsibilities = forms.CharField(widget=forms.Textarea, required=False)
    stack = forms.CharField(widget=forms.TextInput, required=False)
    year_begin = forms.IntegerField(min_value=1950, max_value=now.year, required=True,
                                    label='Год начала')
    year_end = forms.IntegerField(min_value=1950, max_value=now.year, required=False,
                                  label='Оставьте поле пустым, если продолжаете тут работать')
    name = forms.CharField(required=True, label='Наименование организации')
    post = forms.CharField(required=True, label='Должность')

    class Meta:
        model = Experience
        fields = ('post', 'name', 'month_begin', 'year_begin', 'month_end', 'year_end', 'stack', 'responsibilities')

    def __init__(self, *args, **kwargs):
        super(ExperienceCreateForm, self).__init__(*args, **kwargs)
        self.fields['responsibilities'].widget.attrs[
            'placeholder'] = "Опишите Ваши обязанности, навыки и достижения на месте работы"
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        # self.fields['responsibilities'].widget.attrs['class'] = "tinymce"


    def clean_year_end(self):
        """Проверка что дата окончания не больше даты начала"""
        month_begin = format(self.cleaned_data['month_begin'], '02')
        year_begin = str(self.cleaned_data['year_begin'])
        dt1 = time.strptime(year_begin + month_begin + '01', '%Y%m%d')

        year_end = self.cleaned_data.get('year_end', None)
        if year_end:
            month_end = format(self.cleaned_data['month_end'], '02')
            year_end = str(self.cleaned_data['year_end'])
            dt2 = time.strptime(year_end + month_end + '01', '%Y%m%d')
        else:
            year_end = now.year
            dt2 = time.strptime(str(year_end) + format(now.month, '02') + format(now.day, '02'), '%Y%m%d')

        if dt1 > dt2:
            self.add_error('year_end', 'Дата начала не может быть больше даты окончания!')

        return year_end


class EducationCreateForm(forms.ModelForm):
    """форма создания места обучения"""
    name = forms.CharField(max_length=256, required=True, label='Наименование учебного заведения')
    date_end = forms.IntegerField(min_value=1950, required=True, label='Год окончания')
    department = forms.CharField(widget=forms.TextInput, max_length=256, required=True,
                                 label='Факультет')
    specialty = forms.CharField(widget=forms.TextInput, max_length=256, required=False)

    class Meta:
        model = Education
        fields = ('date_end', 'name', 'department', 'specialty')

    def __init__(self, *args, **kwargs):
        super(EducationCreateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        data = self.cleaned_data['name']
        if len(data) > 50:
            raise ValidationError("Название должно быть не более 50 символов.")
        return data


class LanguagesCreateForm(forms.ModelForm):
    """форма создания языка"""
    language = forms.ModelChoiceField(widget=forms.Select(), queryset=Languages.objects.all(),
                                      label='Язык', required=True)
    level = forms.ModelChoiceField(widget=forms.Select(), queryset=LanguageLevels.objects.all(),
                                   label='Уровень', required=True)

    class Meta:
        model = LanguagesSpoken
        fields = ('language', 'level')

    def __init__(self, *args, **kwargs):
        super(LanguagesCreateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'selectpicker'
            field.widget.attrs['data-size'] = '5'
            field.widget.attrs['data-container'] = 'body'

    def clean_language(self):
        cv = CV.objects.filter(id=self.data['cv_id']).first()
        language = Languages.objects.filter(id=self.data['language']).first()
        languages = LanguagesSpoken.objects.filter(cv=cv, language=language)
        if languages:
            self.add_error('language', f'{language} язык уже добавлен Вами в резюме!')
        return language


class LanguagesUpdateForm(forms.ModelForm):
    language = forms.ModelChoiceField(widget=forms.Select(), queryset=Languages.objects.all(),
                                      label='Язык', required=True)
    level = forms.ModelChoiceField(widget=forms.Select(), queryset=LanguageLevels.objects.all(),
                                   label='Уровень', required=True)

    class Meta:
        model = LanguagesSpoken
        fields = ('language', 'level')

    def __init__(self, *args, **kwargs):
        super(LanguagesUpdateForm, self).__init__(*args, **kwargs)
        self.fields['language'].widget.attrs['readonly'] = True
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'selectpicker'
            field.widget.attrs['data-size'] = '5'
            field.widget.attrs['data-container'] = 'body'
