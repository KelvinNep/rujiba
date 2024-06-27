from django import forms
from .models import Survey

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['id', 'nama', 'pertanyaan1', 'pertanyaan2']

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Pilih File Excel (.xlsx, .xls, .csv, .xlsm)')