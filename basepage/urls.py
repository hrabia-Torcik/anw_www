from django.urls import path
from basepage.views import basepage, kursu_zapis, instr_dojazdu, kursy_opisuj, pokaz_polecajki, pokaz_baze_wiedzy, kontaktuj, opisz_dunajca

app_name='basepage'

urlpatterns = [
    path('', basepage),
    path('dojazd/', instr_dojazdu, name='dojazd'),
    path('dunajec/', opisz_dunajca, name='o_dunajcu'),
    path('o_kursach/', kursy_opisuj, name='o_kursach'),
    path('strefa_wiedzy/', pokaz_baze_wiedzy, name='strefa_wiedzy'),
    path('ciekawostki/', pokaz_polecajki, name='ciekawostki'),
    path('kontakt/', kontaktuj, name='kontakt'),
    path('<int:elem_id>', kursu_zapis, name='form_zapis'),
]
