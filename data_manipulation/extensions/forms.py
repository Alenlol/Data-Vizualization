from django import forms
from .models import Document


class UploadFileForm(forms.Form):
    file = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )


class SelectForm(forms.Form):
    new_choice = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_choice'].choices = [(i, j[0]) for i, j in enumerate(Document.objects.values_list('name'))]


