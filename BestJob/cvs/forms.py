from django import forms
import time
import datetime

from cvs.models import CV, Experience, Education, LanguagesSpoken, CVMonths
from search.models import Category, Currency, Languages, LanguageLevels

now = datetime.datetime.now()


class CVCreateForm(forms.ModelForm):
    """форма создание резюме"""
    speciality = forms.ModelChoiceField(widget=forms.Select(), queryset=Category.objects.all().order_by('name'), required=False)
    post = forms.CharField(widget=forms.TextInput, required=False)
    skills = forms.CharField(widget=forms.TextInput, required=False)

    class Meta:
        model = CV
        fields = ('post', 'speciality', 'salary', 'currency', 'education_level', 'moving', 'skills')

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
        fields = ('post', 'speciality', 'salary', 'currency', 'education_level', 'moving', 'skills')

    def __init__(self, *args, **kwargs):
        super(CVUpdateForm, self).__init__(*args, **kwargs)


class ModeratorCVUpdateForm(CVUpdateForm):
    """форма просмотра\редактирования резюме"""
    disabled_fields = ('specialization', 'is_active', 'name', 'experience',
                       'description', 'city', 'description', 'salary_from',
                       'salary_to', 'currency', 'salary_on_hand',)

    class Meta:
        model = CV
        exclude = ('employer_profile',)

    def __init__(self, *args, **kwargs):
        super(ModeratorCVUpdateForm, self).__init__(*args, **kwargs)
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
    year_begin = forms.IntegerField(min_value=1950, max_value=now.year)
    year_end = forms.IntegerField( min_value=1950, max_value=now.year, required=False, label='Оставьте поле пустым, если продолжаете тут работать')

    class Meta:
        model = Experience
        fields = ('post', 'name', 'month_begin','year_begin','month_end','year_end', 'stack', 'responsibilities')


    def __init__(self, *args, **kwargs):
        super(ExperienceCreateForm, self).__init__(*args, **kwargs)
        self.fields['responsibilities'].widget.attrs['placeholder'] = "Опишите Ваши обязанности, навыки и достижения на месте работы"

    def clean_year_end(self):
        month_begin = format(self.cleaned_data['month_begin'], '02')
        year_begin = str(self.cleaned_data['year_begin'])
        month_end = format(self.cleaned_data['month_end'], '02')
        year_end = str(self.cleaned_data['year_end'])
        dt1 = time.strptime(year_begin + month_begin + '01', '%Y%m%d')
        dt2 = time.strptime(year_end + month_end + '01', '%Y%m%d')
        if dt1 > dt2:
            self.add_error('year_end', 'Дата начала не может быть больше дата окончания!')
        return year_end


class EducationCreateForm(forms.ModelForm):
    """форма создания места обучения"""
    date_end = forms.IntegerField(min_value=1950, required=False)
    department = forms.CharField(widget=forms.TextInput, max_length=256, required=False)
    specialty = forms.CharField(widget=forms.TextInput, max_length=256, required=False)

    class Meta:
        model = Education
        fields = ('date_end','name', 'department', 'specialty')

    def __init__(self, *args, **kwargs):
        super(EducationCreateForm, self).__init__(*args, **kwargs)


class LanguagesCreateForm(forms.ModelForm):
    """форма создания языка"""
    language = forms.ModelChoiceField(widget=forms.Select(), queryset=Languages.objects.all())
    level = forms.ModelChoiceField(widget=forms.Select(), queryset=LanguageLevels.objects.all())

    class Meta:
        model = LanguagesSpoken
        fields = ('language','level')

    def __init__(self, *args, **kwargs):
        super(LanguagesCreateForm, self).__init__(*args, **kwargs)

    # def clean_language(self):
    #     language = self.cleaned_data['language']
    #     languages = LanguagesSpoken.objects.filter(cv=self.instance.cv)
    #     if language in languages:
    #         self.add_error('language', f'{language} язык уже добавлен Вами в резюме!')
    #     return language