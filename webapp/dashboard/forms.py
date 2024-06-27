from django import forms

class CustomAdminLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select an Excel file')