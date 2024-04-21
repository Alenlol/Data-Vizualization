from django import forms
from .models import Choices, Document


class UploadFileForm(forms.Form):
    file = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )


class SelectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Gender'].widget.choices = [(i, j[0]) for i, j in enumerate(Document.objects.values_list('name'))]

    class Meta:
        model = Choices
        fields = ('Gender',)

