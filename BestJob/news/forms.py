from django import forms

from news.models import News


class NewsCreateForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(NewsCreateForm, self).__init__(*args, **kwargs)
        self.fields['data'].widget.attrs['placeholder'] = 'Введите data'


class NewsUpdateForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(NewsUpdateForm, self).__init__(*args, **kwargs)
        self.fields['data'].widget.attrs['placeholder'] = 'Введите data'


class NewsDeleteForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(NewsDeleteForm, self).__init__(*args, **kwargs)
        self.fields['data'].widget.attrs['placeholder'] = 'Введите data'
