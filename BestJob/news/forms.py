from django import forms

from news.models import News


class NewsCreateForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'body', 'image']

    def __init__(self, *args, **kwargs):
        super(NewsCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Введите заголовок'
        self.fields['body'].widget.attrs['placeholder'] = 'Введите содержимое'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class NewsUpdateForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput, required=True)
    body = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = News
        fields = ['title', 'body', 'image']

    def __init__(self, *args, **kwargs):
        super(NewsUpdateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Введите заголовок'
        self.fields['body'].widget.attrs['placeholder'] = 'Введите содержимое'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
