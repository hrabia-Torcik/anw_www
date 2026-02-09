from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class XlsxImportForm(forms.Form):
    title = forms.CharField(max_length=50)
    xlsx_dane_upload = forms.FileField()


