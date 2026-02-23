from django.contrib import admin
from .models import WynikAnkiety, OceniajStrone
from django.urls import path
from django.shortcuts import render
from basepage.static.basepage.functions import *
from django import forms
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse

class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = '__all__'


class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = '__all__'




@admin.register(KursyWszystkie)
class KursyWszystkieAdmin(admin.ModelAdmin):
    search_fields = ['kursu_lp', 'kursu_kod', 'kursu_schedule', 'kursu_data_start', 'kursu_data_end', 'kursu_prise', 'kursu_name']  # wpisanie kolejnych pól określających kolumny w bazie danych spowodujemy przeszukiwanie we wszystkich wymienionych kolumnach
    list_display = ['kursu_lp', 'kursu_kod', 'kursu_schedule', 'kursu_data_start', 'kursu_data_end', 'kursu_prise']
    list_filter = ['kursu_schedule', 'kursu_name']

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


@admin.register(WynikAnkiety)
class WynikAnkietyAdmin(admin.ModelAdmin):
    # 1. Kolumny widoczne na liście (w tabeli)
    list_display = ('id', 'czy_polecisz', 'short_uwagi', 'data_wyslania')

    # 2. Filtry po prawej stronie (bardzo przydatne!)
    list_filter = ('czy_polecisz', 'data_wyslania')

    # 3. Wyszukiwarka (szuka w uwagach)
    search_fields = ('uwagi',)

    # 4. Czytelna data na górze (oś czasu)
    date_hierarchy = 'data_wyslania'

    # Funkcja pomocnicza: skraca długie uwagi w tabeli, żeby nie rozciągać wierszy
    def short_uwagi(self, obj):
        if obj.uwagi and len(obj.uwagi) > 50:
            return f"{obj.uwagi[:50]}..."
        return obj.uwagi

    short_uwagi.short_description = 'Uwagi'  # Nagłówek kolumny


@admin.register(OceniajStrone)
class OceniajStroneAdmin(admin.ModelAdmin):
    # 1. Kolumny widoczne na liście (w tabeli)
    list_display = ('id', 'fajnosc', 'czytelnosc', 'co_zmienic', 'co_dodac', 'sugestie')

    # 2. Filtry po prawej stronie (bardzo przydatne!)
    list_filter = ('co_dodac', 'data_wyslania')

    # 3. Wyszukiwarka (szuka w uwagach)
    search_fields = ('sugestie',)

    # 4. Czytelna data na górze (oś czasu)
    date_hierarchy = 'data_wyslania'

    # Funkcja pomocnicza: skraca długie uwagi w tabeli, żeby nie rozciągać wierszy
    def short_uwagi(self, obj):
        if obj.uwagi and len(obj.uwagi) > 50:
            return f"{obj.uwagi[:50]}..."
        return obj.uwagi

    short_uwagi.short_description = 'sugestie'  # Nagłówek kolumny