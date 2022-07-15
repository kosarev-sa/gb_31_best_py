from django import forms
from django.core.exceptions import ValidationError
from django.forms import Textarea

from news.models import News


class NewsCreateForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок', required=True)
    class Meta:
        model = News
        fields = ['title', 'body', 'image']
        widgets = {
            'body': Textarea(attrs={'rows': 7, 'required': True, 'label': 'Текст новости'}),
        }

    def __init__(self, *args, **kwargs):
        super(NewsCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Введите заголовок'
        self.fields['body'].widget.attrs['placeholder'] = 'Введите содержимое'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_title(self):
        data = self.cleaned_data['title']
        if len(data) < 2:
            raise ValidationError("Заголовок должен содержать более одного символа.")
        return data

    def clean_body(self):
        data = self.cleaned_data['body']
        if len(data) < 15:
            raise ValidationError("Текст новости слишком короткий. Минимум - 15 символов.")
        return data


class NewsUpdateForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput, required=True, label='Заголовок')
    body = forms.CharField(widget=forms.Textarea, required=True, label='Содержание')

    class Meta:
        model = News
        fields = ['title', 'body', 'image']

    def __init__(self, *args, **kwargs):
        super(NewsUpdateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Введите заголовок'
        self.fields['body'].widget.attrs['placeholder'] = 'Введите содержимое'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_title(self):
        data = self.cleaned_data['title']
        if len(data) < 2:
            raise ValidationError("Заголовок должен содержать более одного символа.")
        return data

    def clean_body(self):
        data = self.cleaned_data['body']
        if len(data) < 15:
            raise ValidationError("Слишком короткая новость.")
        return data
