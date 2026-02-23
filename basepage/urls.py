from django.urls import path
from basepage.views import (basepage, kursu_zapis, instr_dojazdu, kursy_opisuj,
                            pokaz_polecajki, pokaz_baze_wiedzy, kontaktuj, opisz_dunajca, obsmaruj,
                            ocen_strone, odpowiedz_respondentowi)

app_name='basepage'

urlpatterns = [
    path('', basepage),
    path('dojazd/', instr_dojazdu, name='dojazd'),
    path('Dunajec/', opisz_dunajca, name='o_dunajcu'),
    path('o_kursach/', kursy_opisuj, name='o_kursach'),
    path('strefa_wiedzy/', pokaz_baze_wiedzy, name='strefa_wiedzy'),
    path('polecajki/', pokaz_polecajki, name='polecajki'),
    path('kontakt/', kontaktuj, name='kontakt'),
    path('ankieta/', obsmaruj, name='form_ankiety'),
    path('ocena_strony/', ocen_strone, name='form_oceny'),
    path('poankiecie/', odpowiedz_respondentowi, name='podziekowanie'),
    path('<int:elem_id>', kursu_zapis, name='form_zapis'),
]
