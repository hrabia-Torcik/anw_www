from django.shortcuts import render
from basepage.models import Klientela, UczestUnder18, KursyWszystkie, ZapisyNaKursy, PrzypisOpiekU18, PrzypisanieDoDniaKursu, DniKursowe, Instruktorostwo
from django.template import loader

from django.http import HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime
from datetime import date
from basepage.forms.forms import UploadFileForm
# from somewhere import handle_uploaded_file
import pandas as pd

teraz = datetime.now()
teraz_rok = teraz.strftime("%Y")
teraz_data = teraz.date()
koniec_roku = date(int(teraz_rok), 12, 31)

rok_zalozenia = 1993
liczba_lat = int(teraz_rok) - rok_zalozenia

foremnik = ''
if str(liczba_lat)[-1] in ('1','5','6','7','8','9','0'):
    foremnik = 'lat'
else:
    foremnik = 'lata'

def basepage(request):
    nicnierob = 0
    efekt = 'pusto'


    list_pom = ['','','','','','']
    lista = ['','','','','','']
    context = {}
    flage3 = ''

    # PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
    #
    #
    # if request.method == 'POST':
    #     z_czekboksa = request.POST.get('bez')
    #     z_hidenu = request.POST.get('dod_dane')
    #     lista_00 = z_hidenu.split(',')
    #     for i,elem in enumerate(lista_00):
    #         lista[i]=elem
    #     context['kalarepka0'] = z_czekboksa
    #     context['kalarepka1'] = lista
    #
    #     flage3 = 1
    # context['flage3'] = flage3
    #
    #
    # if request.GET.get('sub1') or (flage3 == 1 and lista[0] != ''):
    #     list_pom[0] ='patent żeglarski'
    #     context['sub1'] = 'cokolwiek'
    # if request.GET.get('sub2') or (flage3 == 1 and lista[1] != ''):
    #     list_pom[1] = 'patent motorowodny'
    #     context['sub2'] = 'cokolwiek'
    # if request.GET.get('sub3') or (flage3 == 1 and lista[2] != ''):
    #     list_pom[2] = 'egzamin żeglarski'
    #     context['sub3'] = 'cokolwiek'
    #     efekt = 'wlazło'
    # if request.GET.get('sub4') or (flage3 == 1 and lista[3] != ''):
    #     list_pom[3] = 'doszk'
    #     context['sub4'] = 'cokolwiek'
    # if request.GET.get('sub5') or (flage3 == 1 and lista[4] != ''):
    #     list_pom[4] = 'jachtowy sternik morski'
    #     context['sub5'] = 'cokolwiek'
    # if request.GET.get('sub6') or (flage3 == 1 and lista[5] != ''):
    #     list_pom[5] = 'lic'
    #     context['sub6'] = 'cokolwiek'
    # if request.GET.get('znak_form1') and any(list_pom) is False:
    #     nicnierob = 1
    #
    # flage4 = ''
    # efekt = nicnierob
    # klienci = Klientela.objects.all()
    # if flage3 == 1:
    #     if z_czekboksa:
    #         kursy = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok).filter(kursu_data_end__range=(teraz_data,koniec_roku))
    #     else:
    #         kursy = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok)
    # else:
    #     if nicnierob == 1:
    #         kursy = KursyWszystkie.objects.all()
    #         flage4 = 1
    #     else:
    #         kursy = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok).filter(kursu_data_end__range=(teraz_data, koniec_roku))
    #
    # # kursy = KursyWszystkie.objects.all()
    # klienciNiedorosli = UczestUnder18.objects.all()
    # zapisy = ZapisyNaKursy.objects.all()
    #
    # kursy_mod = []
    # for elem in kursy:
    #     if elem.kursu_data_start == elem.kursu_data_end:
    #         kursy_mod.append({'nazwa': elem.kursu_name,
    #                           'skrot': elem.kursu_kod,
    #                           'tryb': elem.kursu_schedule,
    #                           'data1': elem.kursu_data_start,
    #                           'data2': '',
    #                           'cena': elem.kursu_prise,
    #                           'id': elem.kursu_lp})
    #     else:
    #         kursy_mod.append({'nazwa': elem.kursu_name,
    #                           'skrot': elem.kursu_kod,
    #                           'tryb': elem.kursu_schedule,
    #                           'data1': elem.kursu_data_start,
    #                           'data2': elem.kursu_data_end,
    #                           'cena': elem.kursu_prise,
    #                           'id': elem.kursu_lp})
    # flage = ''
    # sign = ''
    # sign2 = ''
    #
    # znakL = 0
    # for elem in list_pom:
    #     if elem:
    #         znakL += 1
    #
    # if znakL != 0:
    #     sign2 = 1
    #     kursy_mod_filtrami = []
    #     for elem in kursy_mod:
    #         kursy_mod_filtrami.append([0,elem])
    #     for elem in list_pom:
    #         if elem:
    #             for ind,el in enumerate(kursy_mod_filtrami):
    #                 if (elem == 'doszk' and el[1]['nazwa'].count('doskonalenie') == 1) or (elem == 'doszk' and el[1]['nazwa'].count('manewrowanie') == 1):
    #                     kursy_mod_filtrami[ind][0] = 1
    #                 elif (elem == 'lic' and el[1]['nazwa'].count('SRC') == 1) or (elem == 'lic' and el[1]['nazwa'].count('LRC') == 1):
    #                     kursy_mod_filtrami[ind][0] = 1
    #                 elif el[1]['nazwa'] == elem:
    #                     kursy_mod_filtrami[ind][0] = 1
    #     kursy_mod.clear()
    #     for i,j in enumerate(kursy_mod_filtrami):
    #         if j[0] == 1:
    #             kursy_mod.append(j[1])
    #     flage = 1
    #
    # if znakL == 6:
    #     sign = 1
    #
    #
    #
    #
    #
    # context['kursy_mod'] = kursy_mod
    # context['klienci'] = klienci
    # context['klienciNiedorosli'] = klienciNiedorosli
    # context['zapisy'] = zapisy
    # context['test'] = efekt
    # context['flage'] = flage
    # context['flage4'] = flage4
    # context['sign'] = sign
    # context['sign2'] = sign2
    # context['liczba_lat'] = liczba_lat
    # context['foremnik'] = foremnik
    #
    # PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP

    context['efekt'] = efekt

    takalista = [elemen for elemen in context]

    context['takalista'] = takalista


    return render(request, 'basepage/lists.html', context)

def kursu_zapis(request, elem_id):
    p = KursyWszystkie.objects.get(kursu_lp=elem_id)

    if p.kursu_data_start==p.kursu_data_end:
        wskaznik=''
    else:
        wskaznik=1

    context = {
        'post': p,
        'wskaznik': wskaznik,
        'liczba_lat': liczba_lat,
        'foremnik': foremnik,
    }
    return render(request, 'basepage/form_zapis.html', context)

# Imaginary function to handle an uploaded file.


