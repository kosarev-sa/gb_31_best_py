from django import forms

from news.models import News


class NewsCreateForm(forms.ModelForm):
    class Meta:
        model = News
        exclude = ['author']

    def __init__(self, *args, **kwargs):
        super(NewsCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Введите заголовок'
        self.fields['body'].widget.attrs['placeholder'] = 'Введите содержимое'


class NewsUpdateForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'body', 'is_active']

    def __init__(self, *args, **kwargs):
        super(NewsUpdateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Введите заголовок'
        self.fields['body'].widget.attrs['placeholder'] = 'Введите содержимое'

