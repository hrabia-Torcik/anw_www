from django import forms
from basepage.models import Instruktorostwo


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class XlsxImportForm(forms.Form):
    title = forms.CharField(max_length=50)
    xlsx_dane_upload = forms.FileField()


class AnkietaForm(forms.Form):
    p = Instruktorostwo.objects.values_list('instruktoro_lp', 'instruktoro_name', 'instruktoro_surname')
    list_instr = [({elem[0]},f'{elem[1]} {elem[2][0]}.') for elem in p]

    plec = forms.ChoiceField(
        label="Czy możesz określić swoją płeć?",
        choices=(('0', 'nie odpowiem na to pytanie'), ('K', 'kobieta'), ('M', 'mężczyzna'),
                 ('inna', 'inna opcja')),
        widget=forms.Select(attrs={'class': 'form-select'})
    )


    wiek = forms.ChoiceField(
        label="W jakim jesteś przedziale wiekowym?",
        choices=(('nie', 'nie powiem'), ('nastolatek','14-18 lat'), ('mlody_dorosly','18-30 lat'),
                 ('sredni_wiek', '30-50 lat'), ('pozna_doroslosc', 'niemalże dojrzałym')),
    )

    wybrani_instruktorzy = forms.MultipleChoiceField(
        label="Kto był Twoim instruktoro na jachcie?",
        choices=list_instr,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select ankieta-select',
            'placeholder': 'Wybierz kogoś...'
        })
    )

    czy_polecisz = forms.ChoiceField(
        label="Czy poleciłbyś nas znajomemu?",
        choices=(('tak', 'Tak'), ('tak_ale','tak, ale...'), ('neutralnie','ani tak, ani nie'), ('odradzam', 'odradzałobym'), ('zniechecam', 'bardzo zniechęcało')),
    )

    startowa_wiedza = forms.ChoiceField(
        label="Jaki był poziom Twoich umiejętności przed kursem?",
        choices=(('0', 'Total tabula rasa'), ('1', 'parę razy obserwowałom, jak inni obsługują jacht'),
                 ('2', 'Raz czy dwa razy coś tam porobiłom na jachcie'), ('3', 'Trochę się żeglowało'),('4','Niemałe doświadczenie, również za sterem')),
    )

    nabycie_wiedzy = forms.ChoiceField(
        label="Jak oceniasz przyrost swoich umiejętności w zakresie prowadzenia jachtu?",
        choices=(('super', 'Super'), ('moze_byc', 'Może być'), ('slabo', 'Słabo')),
    )


    prowadzenie_rejsu = forms.ChoiceField(
        label="Czy czujesz się osobą gotową do samodzielnego poprowadzenia rejsu?",
        choices=(('super', 'Tak, spoko to ogarnę'), ('moze_byc', 'Popłynę, ale z duszą na ramieniu'), ('slabo', 'Niespecjalnie')),
    )

    uwagi = forms.CharField(
        label="Dodatkowe uwagi",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )




