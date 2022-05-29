from django import forms

from cvs.models import CV


class CVCreateForm(forms.ModelForm):
    """форма создание резюме"""

    class Meta:
        model = CV
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CVCreateForm, self).__init__(*args, **kwargs)
        self.fields['data'].widget.attrs['placeholder'] = 'Введите data'


class CVUpdateForm(forms.ModelForm):
    """форма просмотра\редактирования резюме"""

    class Meta:
        model = CV
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CVUpdateForm, self).__init__(*args, **kwargs)
        self.fields['data'].widget.attrs['placeholder'] = 'Введите data'


class CVDeleteForm(forms.ModelForm):
    """форма удаления резюме"""

    class Meta:
        model = CV
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CVDeleteForm, self).__init__(*args, **kwargs)
        self.fields['data'].widget.attrs['placeholder'] = 'Введите data'


class CVDistributeForm(forms.ModelForm):
    """форма удаления резюме"""

    class Meta:
        model = CV
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CVDistributeForm, self).__init__(*args, **kwargs)
        self.fields['data'].widget.attrs['placeholder'] = 'Введите data'
