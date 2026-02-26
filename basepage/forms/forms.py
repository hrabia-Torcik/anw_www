from django import forms
from basepage.models import Instruktorostwo, WynikAnkiety, OceniajStrone


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class XlsxImportForm(forms.Form):
    title = forms.CharField(max_length=50)
    xlsx_dane_upload = forms.FileField()


class InstruktorChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        # Tutaj definiujesz co widzi użytkownik
        return f"{obj.instruktoro_name} {obj.instruktoro_surname[0]}."

class AnkietaForm(forms.ModelForm):

    class Meta:
        model = WynikAnkiety
        fields = ['plec', 'wiek', 'wybrani_instruktorzy', 'czy_polecisz', 'startowa_wiedza', 'nabycie_wiedzy', 'prowadzenie_rejsu', 'uwagi']
        widgets = {
            # Django samo weźmie choices z modelu, Ty tylko dokładasz klasę CSS
            'plec': forms.Select(attrs={'class': 'form-select ankieta-select'}),
            'wiek': forms.Select(attrs={'class': 'form-select'}),
            'wybrani_instruktorzy': forms.SelectMultiple(attrs={
            'class': 'form-select ankieta-select',
            'placeholder': 'Wybierz kogoś...',
        }),
            'czy_polecisz': forms.Select(attrs={'class': 'form-select'}),
            'startowa_wiedza': forms.Select(attrs={'class': 'form-select'}),
            'nabycie_wiedzy': forms.Select(attrs={'class': 'form-select'}),
            'prowadzenie_rejsu': forms.Select(attrs={'class': 'form-select'}),
            'uwagi': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TUTAJ przywracasz ładne wyświetlanie imion bez definiowania całego pola od nowa:
        self.fields['wybrani_instruktorzy'].label_from_instance = lambda obj: f"{obj.instruktoro_name} {obj.instruktoro_surname[0]}."
        self.fields['wiek'].empty_label = "wybierz odpowiedź..."
        self.fields['czy_polecisz'].empty_label = "wybierz odpowiedź..."
        self.fields['startowa_wiedza'].empty_label = "wybierz odpowiedź..."
        self.fields['nabycie_wiedzy'].empty_label = "wybierz odpowiedź..."
        self.fields['prowadzenie_rejsu'].empty_label = "wybierz odpowiedź..."

        
class OceniajStroneFORM(forms.ModelForm):

    class Meta:
        model = OceniajStrone

        fields = ['fajnosc', 'czytelnosc', 'co_zmienic', 'co_dodac', 'sugestie']
        widgets = {
            # Django samo weźmie choices z modelu, Ty tylko dokładasz klasę CSS
            'fajnosc': forms.Select(attrs={'class': 'form-select'}),
            'czytelnosc': forms.Select(attrs={'class': 'form-select'}),

            'co_zmienic': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'co_dodac': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sugestie': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TUTAJ przywracasz ładne wyświetlanie imion bez definiowania całego pola od nowa:
        self.fields['fajnosc'].empty_label = "wybierz odpowiedź..."
        self.fields['czytelnosc'].empty_label = "wybierz odpowiedź..."







