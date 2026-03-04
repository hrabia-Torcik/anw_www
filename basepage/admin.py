from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from basepage.static.basepage.functions import *
from django import forms
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .models import WynikAnkiety, OcenaSzczegolowa, OceniajStrone

class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

class FileForm(forms.ModelForm):
    class Meta:
        model = PlikImportu
        fields = '__all__'


class DatasetForm(forms.ModelForm):
    class Meta:
        model = DaneKursuZPliku
        fields = '__all__'




@admin.register(Wydarzenie)
class WydarzenieAdmin(admin.ModelAdmin):

    search_fields = ['kod',
    'schedule',
    'data_start',
    'data_end',
    'price',
    'name']  # wpisanie kolejnych pól określających kolumny w bazie danych spowodujemy przeszukiwanie we wszystkich wymienionych kolumnach
    list_display = ['schedule', 'data_start', 'data_end', 'price']
    list_filter = ['schedule', 'name']

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv), ]
        return new_urls + urls

    def upload_csv(self, request):
        tomika = ''
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")
            tomika = ''
            for x in csv_data:
                fields = x.split(",")
                tomika += fields + '\n'
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form,
                'dane': tomika}
        return render(request, "admin/xlsx_dane_upload.html", data)
        # context = {
        #     'form': file_form,
        #     'lista_zmian': insert_data,
        #     'efekt': efekt,
        #            }

        # return render(request, 'admin/xlsx_dane_upload.html', context)


class OcenaSzczegolowaInline(admin.TabularInline):
    model = OcenaSzczegolowa
    extra = 0  # Nie dodawaj pustych wierszy na starcie
    readonly_fields = ('instruktor', 'ocena_punktualnosc', 'ocena_wiedza', 'ocena_nauczanie', 'ocena_zachowanie')
    can_delete = False # Zablokuj usuwanie pojedynczych ocen z tego poziomu dla


@admin.register(WynikAnkiety)
class WynikAnkietyAdmin(admin.ModelAdmin):
    # # 1. Kolumny widoczne na liście (w tabeli)
    # list_display = ('id', 'czy_polecisz', 'short_uwagi', 'data_wyslania')
    #
    # # 2. Filtry po prawej stronie (bardzo przydatne!)
    # list_filter = ('czy_polecisz', 'data_wyslania')
    #
    # # 3. Wyszukiwarka (szuka w uwagach)
    # search_fields = ('uwagi',)
    #
    # # 4. Czytelna data na górze (oś czasu)
    # date_hierarchy = 'data_wyslania'
    #
    # # Funkcja pomocnicza: skraca długie uwagi w tabeli, żeby nie rozciągać wierszy
    # def short_uwagi(self, obj):
    #     if obj.uwagi and len(obj.uwagi) > 50:
    #         return f"{obj.uwagi[:50]}..."
    #     return obj.uwagi
    #
    # short_uwagi.short_description = 'Uwagi'  # Nagłówek kolumny

#     PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
# Powyższe miałem wpisane samodzielnie

    list_display = ('get_respondent', 'data_wyslania', 'plec_text', 'wiek_text', 'id',)
    list_filter = ('data_wyslania', 'plec', 'wiek')
    inlines = [OcenaSzczegolowaInline]

    # Metody pomocnicze do wyświetlania tekstów zamiast cyfr w tabeli
    def plec_text(self, obj):
        return obj.get_plec_display()
    plec_text.short_description = "Płeć"

    def wiek_text(self, obj):
        return obj.get_wiek_display()
    wiek_text.short_description = "Wiek"

    def get_respondent(self, obj):
        # Tu możemy wrócić do Twojej funkcji 'znajdz_odmiane'!
        return f"Ankieta #{obj.id}"
    get_respondent.short_description = "Respondent"

    def has_change_permission(self, request, obj=None):
        if obj: # Blokujemy zmianę istniejących rekordów
            return False
        return super().has_change_permission(request, obj)

    def has_add_permission(self, request):
        """Ukrywa przycisk 'Dodaj Wynik ankiety' w adminie."""
        return False

    def has_change_permission(self, request, obj=None):
        """Zmienia tryb edycji na podgląd (wszystkie pola stają się readonly)."""
        return False

    # def has_delete_permission(self, request, obj=None):
    #     """Opcjonalnie: blokuje usuwanie ankiet z panelu admina."""
    #     return False

@admin.register(OcenaSzczegolowa)
class OcenaSzczegolowaAdmin(admin.ModelAdmin):



    list_display = ('instruktor', 'punktualnosc_header', 'wiedza_header', 'nauczanie_header', 'zachowanie_header', 'get_ankieta_date', 'id')
    list_filter = ('instruktor',)

    def get_ankieta_date(self, obj):
        return obj.ankieta.data_wyslania

    def get_ocena_punktualnosc(self, obj):
        return obj.ocena_punktualnosc

    get_ankieta_date.short_description = "Data wysłania"
    get_ankieta_date.admin_order_field = 'ankieta__data_wyslania'  # Pozwala sortować po dacie

    def punktualnosc_header(self, obj):
        return obj.ocena_punktualnosc

    def wiedza_header(self, obj):
        return obj.ocena_wiedza

    def nauczanie_header(self, obj):
        return obj.ocena_nauczanie

    def zachowanie_header(self, obj):
        return obj.ocena_zachowanie

    punktualnosc_header.short_description = "Punktualność"  # Twój nowy nagłówek
    wiedza_header.short_description = "Wiedza"  # Twój nowy nagłówek
    nauczanie_header.short_description = "Nauczanie"  # Twój nowy nagłówek
    zachowanie_header.short_description = "Styl bycia"  # Twój nowy nagłówek

    def has_change_permission(self, request, obj=None):
        if obj: # Blokujemy zmianę istniejących rekordów
            return False
        return super().has_change_permission(request, obj)

    def has_add_permission(self, request):
        """Ukrywa przycisk 'Dodaj Wynik ankiety' w adminie."""
        return False

    def has_change_permission(self, request, obj=None):
        """Zmienia tryb edycji na podgląd (wszystkie pola stają się readonly)."""
        return False

    # def has_delete_permission(self, request, obj=None):
    #     """Opcjonalnie: blokuje usuwanie ankiet z panelu admina."""
    #     return False





    class Meta:
        verbose_name = "Ocena instruktoro"
        verbose_name_plural = "Oceny instruktorostwa"

@admin.register(OceniajStrone)
class OceniajStroneAdmin(admin.ModelAdmin):
    
    # 1. Kolumny widoczne na liście (w tabeli)
    list_display = ('co_zmienic', 'co_dodac', 'sugestie','fajnosc', 'czytelnosc', 'id',)

    # 2. Filtry po prawej stronie (bardzo przydatne!)
    list_filter = ('fajnosc', 'czytelnosc',)

    # 3. Wyszukiwarka (szuka w uwagach)
    search_fields = ('sugestie',)

    # 4. Czytelna data na górze (oś czasu)
    date_hierarchy = 'data_wyslania'

    # Funkcja pomocnicza: skraca długie uwagi w tabeli, żeby nie rozciągać wierszy
    def short_co_zmienic(self, obj):
        if obj.co_zmienic and len(obj.co_zmienic) > 50:
            return f"{obj.co_zmienic[:50]}..."
        return obj.co_zmienic
    
    def short_co_dodac(self, obj):
        if obj.co_dodac and len(obj.co_dodac) > 50:
            return f"{obj.co_dodac[:50]}..."
        return obj.co_dodac
    
    def short_sugestie(self, obj):
        if obj.sugestie and len(obj.sugestie) > 50:
            return f"{obj.sugestie[:50]}..."
        return obj.sugestie

    def has_add_permission(self, request):
        """Ukrywa przycisk 'Dodaj Wynik ankiety' w adminie."""
        return False

    def has_change_permission(self, request, obj=None):
        """Zmienia tryb edycji na podgląd (wszystkie pola stają się readonly)."""
        return False

    # def has_delete_permission(self, request, obj=None):
    #     """Opcjonalnie: blokuje usuwanie ankiet z panelu admina."""
    #     return False


    short_co_zmienic.short_description = 'do zmienienia'  # Nagłówek kolumny
    short_co_dodac.short_description = 'dodaj takie'  # Nagłówek kolumny
    short_sugestie.short_description = 'sugestie'  # Nagłówek kolumny

@admin.register(Instruktor)
class InstruktorAdmin(admin.ModelAdmin):

    list_display = (
                    # 'instruktoro_name',
                    # 'instruktoro_name_dopelniacz',
                    'nazwisko',
                    'imie',
                    'telefon',
                    'email',
                    'stopien',
                    'id',)


    # 2. Filtry po prawej stronie (bardzo przydatne!)
    list_filter = ('stopien',)

    # search_fields = ('nazwisko',)
    # search_fields = ('stopien',)

@admin.register(Klient)
class InstruktorAdmin(admin.ModelAdmin):

    list_display = (
                    'nazwisko',
                    'imie',
                    'telefon',
                    'email',
                    'id',)


    # 2. Filtry po prawej stronie (bardzo przydatne!)
    search_fields = ('telefon','nazwisko')

    # search_fields = ('nazwisko',)
    # search_fields = ('stopien',)


