from django.shortcuts import render, redirect
from basepage.models import Klientela, UczestUnder18, KursyWszystkie, ZapisyNaKursy, PrzypisOpiekU18, PrzypisanieDoDniaKursu, DniKursowe, Instruktorostwo
from django.template import loader

from django.http import HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime, timedelta
from datetime import date
from basepage.forms.forms import AnkietaForm
# from somewhere import handle_uploaded_file
import pandas as pd

from django.contrib import messages

teraz_data = datetime.now().date()
# teraz_data = date(2026, 12, 22)
teraz_rok = teraz_data.strftime("%Y")
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
    napis = ''
    z_czekboksa = ''


    if request.method == 'POST':
        z_czekboksa = request.POST.get('bez')
        z_hidenu = request.POST.get('dod_dane')
        lista_00 = z_hidenu.split(',')
        for i,elem in enumerate(lista_00):
            lista[i]=elem
        context['kalarepka0'] = z_czekboksa
        context['kalarepka1'] = lista

        flage3 = 1
        messages.success(request, "Formularz wysłany!", extra_tags='zakonczone')

    context['flage3'] = flage3


    if request.GET.get('sub1') or (flage3 == 1 and lista[0] != ''):
        list_pom[0] ='patent żeglarski'
        context['sub1'] = 'cokolwiek'
    if request.GET.get('sub2') or (flage3 == 1 and lista[1] != ''):
        list_pom[1] = 'patent motorowodny'
        context['sub2'] = 'cokolwiek'
    if request.GET.get('sub3') or (flage3 == 1 and lista[2] != ''):
        list_pom[2] = 'egzamin żeglarski'
        context['sub3'] = 'cokolwiek'
        efekt = 'wlazło'
    if request.GET.get('sub4') or (flage3 == 1 and lista[3] != ''):
        list_pom[3] = 'doszk'
        context['sub4'] = 'cokolwiek'
    if request.GET.get('sub5') or (flage3 == 1 and lista[4] != ''):
        list_pom[4] = 'jachtowy sternik morski'
        context['sub5'] = 'cokolwiek'
    if request.GET.get('sub6') or (flage3 == 1 and lista[5] != ''):
        list_pom[5] = 'lic'
        context['sub6'] = 'cokolwiek'
    if request.GET.get('znak_form1') and any(list_pom) is False:
        nicnierob = 1

    if request.GET:  # Sprawdzasz czy filtry działają
        messages.info(request, "Filtry zastosowane", extra_tags='wybrane')

    """
    Tu poniej jest podstawowy mechanizm zasysania danych o kursach z bazy.
    flage3 jest na wypadek uruchomienia formularza POST, który informuje o chęci wyświetlenia zakończonych kursów.
    nicnierob jest na okoliczność niezaznaczenia niczego do wyświetlenia.
    """

    flage4 = ''
    jestKursWPrzeszlosci = ''
    nieMaJuzKursuWPlanach = ''

    liczba_wszystkich = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok).count()

    liczba_poDzisiaju = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok).filter(
                kursu_data_start__range=((teraz_data + timedelta(days=1)), koniec_roku)).count()

    liczba_zak = liczba_wszystkich - liczba_poDzisiaju

    if liczba_poDzisiaju == 0:
        nieMaJuzKursuWPlanach = 'kabanos'

    if liczba_zak > 0:
        jestKursWPrzeszlosci = 'herbatka'


    if flage3 == 1:
        if z_czekboksa:
            kursy = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok)
        else:
            kursy = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok).filter(
                kursu_data_start__range=((teraz_data + timedelta(days=1)), koniec_roku))

    else:
        if nicnierob == 1:
            kursy = {}
            flage4 = 1
        else:
            kursy = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok).filter(
                kursu_data_start__range=((teraz_data + timedelta(days=1)), koniec_roku))
            if liczba_poDzisiaju == 0:
                kursy = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok)





    # kursy = KursyWszystkie.objects.all()
    # klienciNiedorosli = UczestUnder18.objects.all()
    # zapisy = ZapisyNaKursy.objects.all()

    kursy_mod = []
    for elem in kursy:
        if elem.kursu_data_start == elem.kursu_data_end:
            kursy_mod.append({'nazwa': elem.kursu_name,
                              'skrot': elem.kursu_kod,
                              'tryb': elem.kursu_schedule,
                              'data1': elem.kursu_data_start,
                              'data2': '',
                              'cena': elem.kursu_prise,
                              'id': elem.kursu_lp})
        else:
            kursy_mod.append({'nazwa': elem.kursu_name,
                              'skrot': elem.kursu_kod,
                              'tryb': elem.kursu_schedule,
                              'data1': elem.kursu_data_start,
                              'data2': elem.kursu_data_end,
                              'cena': elem.kursu_prise,
                              'id': elem.kursu_lp})
    flage = ''
    sign = ''
    sign2 = ''

    znakL = 0
    for elem in list_pom:
        if elem:
            znakL += 1

    if znakL != 0:
        sign2 = 1
        kursy_mod_filtrami = []
        for elem in kursy_mod:
            kursy_mod_filtrami.append([0,elem])
        for elem in list_pom:
            if elem:
                for ind,el in enumerate(kursy_mod_filtrami):
                    if (elem == 'doszk' and el[1]['nazwa'].count('doskonalenie') == 1) or (elem == 'doszk' and el[1]['nazwa'].count('manewrowanie') == 1):
                        kursy_mod_filtrami[ind][0] = 1
                    elif (elem == 'lic' and el[1]['nazwa'].count('SRC') == 1) or (elem == 'lic' and el[1]['nazwa'].count('LRC') == 1):
                        kursy_mod_filtrami[ind][0] = 1
                    elif el[1]['nazwa'] == elem:
                        kursy_mod_filtrami[ind][0] = 1
        kursy_mod.clear()
        for i,j in enumerate(kursy_mod_filtrami):
            if j[0] == 1:
                kursy_mod.append(j[1])
        flage = 1

    if znakL == 6:
        sign = 1

    if nieMaJuzKursuWPlanach:

        napis = '<span class="fs-3">Niczego już nie mamy w planach w tym roku.</span><br> Ale zobacz, ile się działo! Jeśli chcesz wiedzieć, co będzie w przyszłym roku - napisz do nas.'
    elif flage4:
        napis = "Niczego nie&nbsp;pokazuję. A&nbsp;może by tak coś zaznaczyć?"
    else:
        if sign:
            napis = "Pokazuję listę zaplanowanych przez nas do&nbsp;końca roku kursów i&nbsp;egzaminów:"
        else:
            if flage:
                napis = "Pokazuję przefiltrowaną listę tegorocznych wydarzeń:"
            else:
                napis = "Pokazuję listę zaplanowanych przez nas do&nbsp;końca roku kursów i&nbsp;egzaminów:"

    if z_czekboksa:
        napis += '<br>Pokazuję również zakończone oraz trwające wydarzenia.'

    kursy_mod.sort(key=lambda x: x['data1'])
    lista_trwaj = []
    lista_zakoncz = []
    for elem in kursy_mod:
        deltat1 = elem['data1'] - teraz_data
        if elem['data2']:
            deltat2 = elem['data2'] - teraz_data
        else:
            deltat2 = False

        if deltat2 or deltat2 == timedelta(0):
            if deltat1 <= timedelta(0) and deltat2 >= timedelta(0):
                lista_trwaj.append(True)
            else:
                lista_trwaj.append(False)
            if deltat2 < timedelta(0):
                lista_zakoncz.append(True)
            else:
                lista_zakoncz.append(False)
        else:
            if deltat1 == timedelta(0):
                lista_trwaj.append(True)
            else:
                lista_trwaj.append(False)
            if deltat1 < timedelta(0):
                lista_zakoncz.append(True)
            else:
                lista_zakoncz.append(False)

    index_zaplanowane = None
    for i, elem in enumerate(kursy_mod):
        deltat1 = elem['data1'] - teraz_data
        if deltat1 >= timedelta(0):
            index_zaplanowane = i + 1
            break



    dane_powiazane = zip(kursy_mod, lista_trwaj, lista_zakoncz)

    context['kursy_mod'] = dane_powiazane
    context['do_kotwicy2'] = index_zaplanowane
    context['test'] = efekt
    context['flage'] = flage
    context['flage4'] = flage4
    context['napis'] = napis
    context['sign'] = sign
    context['sign2'] = sign2
    context['liczba_lat'] = liczba_lat
    context['foremnik'] = foremnik
    context['jest_przeszlosc'] = jestKursWPrzeszlosci
    context['bez_przyszlosci'] = nieMaJuzKursuWPlanach

    # PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP

    # context['efekt'] = [lista_trwaj,len(lista_trwaj),lista_zakoncz,len(lista_zakoncz)]
    # context['efekt'] = kursy_mod
    # context['efekt'] = index_zaplanowane
    # context['efekt2'] = teraz_data, f"długość listy kursy: {len(kursy)}"

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

def instr_dojazdu(request):

    napis = 'Tu będzie coś o dojeździe.'

    context = {
        'text': napis,

        'liczba_lat': liczba_lat,
        'foremnik': foremnik,
    }
    return render(request, 'basepage/dojazd.html', context)


def opisz_dunajca(request):
    napis = 'Tu będzie coś o naszym Dunajcu.'

    context = {
        'text': napis,

        'liczba_lat': liczba_lat,
        'foremnik': foremnik,
    }
    return render(request, 'basepage/dunajec.html', context)


def kursy_opisuj(request):
    napis = 'Tu będzie coś o kursach.'

    context = {
        'text': napis,

        'liczba_lat': liczba_lat,
        'foremnik': foremnik,
    }
    return render(request, 'basepage/kursy.html', context)


def pokaz_baze_wiedzy(request):
    napis = 'Tu będzie coś do pouczenia.'

    context = {
        'text': napis,

        'liczba_lat': liczba_lat,
        'foremnik': foremnik,
    }
    return render(request, 'basepage/wiedza.html', context)

def pokaz_polecajki(request):
    napis = 'Tu będą jakieś pożyteczne linki.'

    context = {
        'text': napis,

        'liczba_lat': liczba_lat,
        'foremnik': foremnik,
    }
    return render(request, 'basepage/polecajki.html', context)

def kontaktuj(request):
    napis = 'Tu będą nasze mejle i telefony.'

    context = {
        'text': napis,

        'liczba_lat': liczba_lat,
        'foremnik': foremnik,
    }
    return render(request, 'basepage/kontakt.html', context)

def obsmaruj(request):
    napis = ('Poświęć proszę trochę czasu i daj nam znać, jakie są Twoje wrażenia po szkoleniu. To nam bardzo pomoże.'
             '<br><span class="fs-3">Szczególnie zależy nam, żeby wiedzieć, jeśli coś Ci się nie podobało.</span>')

    p = Instruktorostwo.objects.values_list('instruktoro_name', 'instruktoro_surname')
    list_instr = [((i + 1), f'{elem[0]} {elem[1][0]}.') for i, elem in enumerate(p)]

    if request.method == 'POST':
        form = AnkietaForm(request.POST)
        if form.is_valid():
            # Django już wyczyściło dane!
            dane = form.cleaned_data['wybrani_instruktorzy']
            for inst_id in dane:
                # Wyciągamy dynamiczne pola po nazwie zdefiniowanej w JS
                punktualnosc = request.POST.get(f'ocena_punktualnosc_{inst_id}')
                wiedza = request.POST.get(f'ocena_wiedza_{inst_id}')

                # Tutaj zapisujesz do bazy (np. do modelu Ocena)
                print(f"Instruktor {inst_id}: Punktualność {punktualnosc}, Wiedza {wiedza}")

            return redirect('success_url')
    else:
        form = AnkietaForm()

    context = {
        'text': napis,
        'instruktorostwo': list_instr,
        'form': form,

        'liczba_lat': liczba_lat,
        'foremnik': foremnik,
    }
    return render(request, 'basepage/ankieta.html', context)