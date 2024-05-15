from django import forms
from .models import Document


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['docfile']


class SelectForm(forms.Form):
    new_choice = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        value_choices = kwargs.pop('values', 0)

        super(SelectForm, self).__init__(*args, **kwargs)
        self.fields['new_choice'].choices = [(i, j[0]) for i, j in enumerate(value_choices)]


class SelectColumnForm(forms.Form):
    original_field = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 0)
        value_choices = kwargs.pop('values', 0)

        super(SelectColumnForm, self).__init__(*args, **kwargs)
        self.fields['original_field'].choices = value_choices

        for index in range(extra_fields):
            self.fields['extra_field_{index}'.format(index=index)] = \
                forms.ChoiceField(choices=value_choices)


class SelectColumnFormY(forms.Form):
    y_field = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        value_choices = kwargs.pop('values', 0)

        super(SelectColumnFormY, self).__init__(*args, **kwargs)
        self.fields['y_field'].choices = value_choices


class SelectDataForm(forms.Form):
    choosed_type = forms.RadioSelect()