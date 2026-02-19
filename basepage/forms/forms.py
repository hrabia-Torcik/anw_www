from django import forms
from basepage.models import Instruktorostwo


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class XlsxImportForm(forms.Form):
    title = forms.CharField(max_length=50)
    xlsx_dane_upload = forms.FileField()


class AnkietaForm(forms.Form):
    p = Instruktorostwo.objects.values_list('instruktoro_name', 'instruktoro_surname')
    list_instr = [((i +1),f'{elem[0]} {elem[1][0]}.') for i,elem in enumerate(p)]

    wybrani_instruktorzy = forms.MultipleChoiceField(
        label="Kto był Twoim instruktorem na jachcie?",
        choices=list_instr,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select ankieta-select',
            'placeholder': 'Wybierz kogoś...'
        })
    )
    uwagi = forms.CharField(
        label="Dodatkowe uwagi",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )


