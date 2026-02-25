from django.shortcuts import render, redirect
from basepage.models import (Klientela, UczestUnder18, KursyWszystkie, ZapisyNaKursy, PrzypisOpiekU18,
                             PrzypisanieDoDniaKursu, DniKursowe, Instruktorostwo, OcenaSzczegolowa)
from django.template import loader

from django.http import HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime, timedelta
from datetime import date
from basepage.forms.forms import AnkietaForm, OceniajStroneFORM
# from somewhere import handle_uploaded_file
import pandas as pd

from django.contrib import messages

teraz_data = datetime.now().date()
# teraz_data = date(2026, 12, 22)
teraz_rok = teraz_data.strftime("%Y")
poczatek_roku = date(int(teraz_rok), 1, 1)
koniec_roku = date(int(teraz_rok), 12, 31)

rok_zalozenia = 1993
liczba_lat = int(teraz_rok) - rok_zalozenia

foremnik = ''
if str(liczba_lat)[-1] in ('1', '5', '6', '7', '8', '9', '0'):
    foremnik = 'lat'
else:
    foremnik = 'lata'


def basepage(request):
    '''
    Tu są funkcje przeszukujące bazę danych dla konkretnego rodzaju wydarzenia w ZADANYM PRZEDZIALE CZASU.
    Póżniej w zależności od potrzeb ich wyniki są sumowane.
    '''

    def znajdz_PZ_Wczasie(kursy, data1):
        qs1 = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok).filter(
            kursu_name__contains='patent żeglarski').filter(
            kursu_data_start__range=(data1, koniec_roku))
        if kursy:
            kursy = kursy | qs1
        else:
            kursy = qs1

        return kursy

    def znajdz_SM_Wczasie(kursy, data1):
        qs1 = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok).filter(
            kursu_name__contains='patent motorowodny').filter(
            kursu_data_start__range=(data1, koniec_roku))
        if kursy:
            kursy = kursy | qs1
        else:
            kursy = qs1

        return kursy

    def znajdz_EG_Wczasie(kursy, data1):
        qs1 = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok).filter(
            kursu_name__contains='egzamin żeglarski').filter(
            kursu_data_start__range=(data1, koniec_roku))
        if kursy:
            kursy = kursy | qs1
        else:
            kursy = qs1

        return kursy

    def znajdz_MA_Wczasie(kursy, data1):
        qs1a = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok).filter(
            kursu_name__contains='manewrowanie').filter(
            kursu_data_start__range=(data1, koniec_roku))
        qs1b = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok).filter(
            kursu_name__contains='doskonalenie').filter(
            kursu_data_start__range=(data1, koniec_roku))
        if qs1a and qs1b:
            qs1 = qs1a | qs1b
        elif qs1a:
            qs1 = qs1a
        elif qs1b:
            qs1 = qs1b

        if kursy:
            kursy = kursy | qs1
        else:
            kursy = qs1

        return kursy

    def znajdz_JSM_Wczasie(kursy, data1):
        qs1 = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok).filter(
            kursu_name__contains='jachtowy sternik morski').filter(
            kursu_data_start__range=(data1, koniec_roku))
        if kursy:
            kursy = kursy | qs1
        else:
            kursy = qs1

        return kursy

    def znajdz_RC_Wczasie(kursy, data1):
        qs1 = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok).filter(
            kursu_name__contains='licencja').filter(
            kursu_data_start__range=(data1, koniec_roku))
        if kursy:
            kursy = kursy | qs1
        else:
            kursy = qs1

        return kursy

    nicnierob = 0
    efekt = 'pusto'
    kursy = ''

    list_pom = ['', '', '', '', '', '']
    lista = ['', '', '', '', '', '']
    context = {}
    flage3 = ''
    flage4 = ''
    napis = ''
    z_czekboksa = ''

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

    if request.method == 'POST':
        z_czekboksa = request.POST.get('bez')
        z_hidenu = request.POST.get('dod_dane')
        lista_00 = z_hidenu.split(',')
        for i, elem in enumerate(lista_00):
            lista[i] = elem
        context['kalarepka0'] = z_czekboksa
        context['kalarepka1'] = lista

        flage3 = 1

        if z_hidenu:
            for i, elem in enumerate(lista):
                if elem:
                    if z_czekboksa:
                        if i == 0:
                            kursy = znajdz_PZ_Wczasie(kursy, poczatek_roku)
                        elif i == 1:
                            kursy = znajdz_SM_Wczasie(kursy, poczatek_roku)
                        elif i == 2:
                            kursy = znajdz_EG_Wczasie(kursy, poczatek_roku)
                        elif i == 3:
                            kursy = znajdz_MA_Wczasie(kursy, poczatek_roku)
                        elif i == 4:
                            kursy = znajdz_JSM_Wczasie(kursy, poczatek_roku)
                        elif i == 5:
                            kursy = znajdz_RC_Wczasie(kursy, poczatek_roku)

                    else:
                        if i == 0:
                            kursy = znajdz_PZ_Wczasie(kursy, (teraz_data + timedelta(days=1)))
                        elif i == 1:
                            kursy = znajdz_SM_Wczasie(kursy, (teraz_data + timedelta(days=1)))
                        elif i == 2:
                            kursy = znajdz_EG_Wczasie(kursy, (teraz_data + timedelta(days=1)))
                        elif i == 3:
                            kursy = znajdz_MA_Wczasie(kursy, (teraz_data + timedelta(days=1)))
                        elif i == 4:
                            kursy = znajdz_JSM_Wczasie(kursy, (teraz_data + timedelta(days=1)))
                        elif i == 5:
                            kursy = znajdz_RC_Wczasie(kursy, (teraz_data + timedelta(days=1)))
        else:
            if z_czekboksa:
                kursy = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok)
            else:
                kursy = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok).filter(
                    kursu_data_start__range=((teraz_data + timedelta(days=1)), koniec_roku))

        messages.success(request, "Formularz wysłany!", extra_tags='zakonczone')

    if request.GET:  # Sprawdzasz czy filtry działają
        messages.info(request, "Filtry zastosowane", extra_tags='wybrane')

    if request.GET.get('sub1') or (flage3 == 1 and lista[0] != ''):
        list_pom[0] = 'patent żeglarski'
        context['sub1'] = 'cokolwiek'

        kursy = znajdz_PZ_Wczasie(kursy, (teraz_data + timedelta(days=1)))

    if request.GET.get('sub2') or (flage3 == 1 and lista[1] != ''):
        list_pom[1] = 'patent motorowodny'
        context['sub2'] = 'cokolwiek'
        kursy = znajdz_SM_Wczasie(kursy, (teraz_data + timedelta(days=1)))

    if request.GET.get('sub3') or (flage3 == 1 and lista[2] != ''):
        list_pom[2] = 'egzamin żeglarski'
        context['sub3'] = 'cokolwiek'
        kursy = znajdz_EG_Wczasie(kursy, (teraz_data + timedelta(days=1)))

    if request.GET.get('sub4') or (flage3 == 1 and lista[3] != ''):
        list_pom[3] = 'doszk'
        context['sub4'] = 'cokolwiek'
        kursy = znajdz_MA_Wczasie(kursy, (teraz_data + timedelta(days=1)))

    if request.GET.get('sub5') or (flage3 == 1 and lista[4] != ''):
        list_pom[4] = 'jachtowy sternik morski'
        context['sub5'] = 'cokolwiek'
        kursy = znajdz_JSM_Wczasie(kursy, (teraz_data + timedelta(days=1)))

    if request.GET.get('sub6') or (flage3 == 1 and lista[5] != ''):
        list_pom[5] = 'lic'
        context['sub6'] = 'cokolwiek'
        kursy = znajdz_RC_Wczasie(kursy, (teraz_data + timedelta(days=1)))

    if request.GET.get('znak_form1') and any(list_pom) is False:
        nicnierob = 1

    if nicnierob == 1:
        kursy = {}
        flage4 = 1

    if kursy == '':
        if liczba_poDzisiaju == 0:
            kursy = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok)
        else:
            kursy = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok).filter(
                kursu_data_start__range=((teraz_data + timedelta(days=1)), koniec_roku))

    context['flage3'] = flage3

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
    suma_licznikow = ''

    znakL = 0
    for elem in list_pom:
        if elem:
            znakL += 1
    liczniki_dlugosci = ['', '', '', '', '', '']
    if znakL != 0:
        sign2 = 1
        kursy_mod_filtrami = []
        suma_licznikow = 0
        for elem in kursy_mod:
            kursy_mod_filtrami.append([0, elem])
        for u, elem in enumerate(list_pom):
            if elem:

                if u == 0:
                    liczba = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok).filter(
                        kursu_name=('patent żeglarski')).count()
                    liczniki_dlugosci[0] = liczba
                    suma_licznikow += liczba
                if u == 1:
                    liczba = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok).filter(
                        kursu_name=('patent motorowodny')).count()
                    liczniki_dlugosci[1] = liczba
                    suma_licznikow += liczba
                if u == 2:
                    liczba = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok).filter(
                        kursu_name=('egzamin żeglarski')).count()
                    liczniki_dlugosci[2] = liczba
                    suma_licznikow += liczba
                if u == 3:
                    liczba1 = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok).filter(
                        kursu_name__icontains='manewrowanie').count()
                    liczba2 = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok).filter(
                        kursu_name__icontains='doskonalenie').count()
                    liczniki_dlugosci[3] = liczba1 + liczba2
                    suma_licznikow += (liczba1 + liczba2)
                if u == 4:
                    liczba = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok).filter(
                        kursu_name=('jachtowy sternik morski')).count()
                    liczniki_dlugosci[4] = liczba
                    suma_licznikow += liczba
                if u == 5:
                    liczba = KursyWszystkie.objects.filter(kursu_data_start__contains=teraz_rok).filter(
                        kursu_name__icontains=('licencja')).count()
                    liczniki_dlugosci[5] = liczba
                    suma_licznikow += liczba
                for ind, el in enumerate(kursy_mod_filtrami):
                    if (elem == 'doszk' and el[1]['nazwa'].count('doskonalenie') == 1) or (
                            elem == 'doszk' and el[1]['nazwa'].count('manewrowanie') == 1):
                        kursy_mod_filtrami[ind][0] = 1
                    elif (elem == 'lic' and el[1]['nazwa'].count('SRC') == 1) or (
                            elem == 'lic' and el[1]['nazwa'].count('LRC') == 1):
                        kursy_mod_filtrami[ind][0] = 1
                    elif el[1]['nazwa'] == elem:
                        kursy_mod_filtrami[ind][0] = 1
        kursy_mod.clear()
        for i, j in enumerate(kursy_mod_filtrami):
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
            napis = "Pokazuję zaplanowane przez nas do&nbsp;końca roku kursy i&nbsp;egzaminy"
        else:
            if flage:
                napis = "Pokazuję przefiltrowane tegoroczne wydarzenia:"
            else:
                napis = "Pokazuję zaplanowane przez nas do&nbsp;końca roku kursy i&nbsp;egzaminy:"

    if z_czekboksa:
        napis = napis[:-1]
        napis += '.<br>Pokazuję również zakończone oraz (jeśli są) trwające wydarzenia:'

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

    if suma_licznikow:
        if suma_licznikow == len(kursy_mod):
            jestKursWPrzeszlosci = ''
        if z_czekboksa:
            jestKursWPrzeszlosci = 'kalarepka'

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
    context['efekt2'] = list_pom
    # context['efekt3'] = liczniki_dlugosci, suma_licznikow
    context['efekt3'] = kursy
    # context['efekt'] = index_zaplanowane
    # context['efekt2'] = teraz_data, f"długość listy kursy: {len(kursy)}"
    context['efekt'] = teraz_data, f"długość listy kursy: {len(kursy)}"

    # takalista = [elemen for elemen in context]
    #
    # context['takalista'] = takalista

    return render(request, 'basepage/lists.html', context)


def kursu_zapis(request, elem_id):
    p = KursyWszystkie.objects.get(kursu_lp=elem_id)

    if p.kursu_data_start == p.kursu_data_end:
        wskaznik = ''
    else:
        wskaznik = 1

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
    napis = ('Historia statku Dunajec sprawia, że korzystanie z jego pokładu podczas szkoleń jest nie tylko przyjemnością,'
             ' ale i wyjątkowym doznaniem.')

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
    context = {}
    napis = ('<p>Poświęć proszę 3 minuty i daj nam znać, jakie są Twoje wrażenia po szkoleniu.</p>'
             '<p class="fs-3 mt-3">Szczególnie zależy nam, żeby wiedzieć, jeśli coś Ci się nie podobało.</p>')

    p = Instruktorostwo.objects.values_list('instruktoro_name', 'instruktoro_surname')
    list_instr = [((i + 1), f'{elem[0]} {elem[1][0]}.') for i, elem in enumerate(p)]

    if request.method == 'POST':
        form = AnkietaForm(request.POST)
        if form.is_valid():
            # 2. Zapisujemy główne dane (czy_polecisz, uwagi, instruktorzy)
            # form.save() automatycznie obsłuży tabelę ManyToMany
            ankieta_instancja = form.save()
            # 3. Wyłapujemy DYNAMICZNE oceny z suwaków (range)
            # Pobieramy listę ID wybranych instruktorów
            wybrani_id = request.POST.getlist('wybrani_instruktorzy')

            for inst_id in wybrani_id:
                # Szukamy oceny po nazwie, którą nadaliśmy w JS: ocena_wiedza_${id}
                ocena_punktualnosc_wartosc = request.POST.get(f'ocena_punktualnosc_{inst_id}')
                ocena_wiedza_wartosc = request.POST.get(f'ocena_wiedza_{inst_id}')
                ocena_nauczania_wartosc = request.POST.get(f'ocena_nauczania_{inst_id}')
                ocena_atmosfery_wartosc = request.POST.get(f'ocena_atmosfery_{inst_id}')

                if ocena_wiedza_wartosc and ocena_punktualnosc_wartosc:
                    # Tutaj na razie wypiszemy to w konsoli serwera,
                    # żebyś widział, że "dolatuje":
                    print(
                        f"Instruktor ID {inst_id} otrzymał ocenę umiejętności nauczania: {ocena_wiedza_wartosc}, natomiast atmosfery: {ocena_atmosfery_wartosc}.")

                    OcenaSzczegolowa.objects.create(
                        ankieta=ankieta_instancja,
                        instruktor_id=int(inst_id),
                        ocena_punktualnosc=int(ocena_punktualnosc_wartosc),
                        ocena_wiedza=int(ocena_wiedza_wartosc),
                        ocena_nauczanie=int(ocena_nauczania_wartosc),
                        ocena_zachowanie=int(ocena_atmosfery_wartosc)
                    )

            return redirect('basepage:podziekowanie')
        else:
            context['post_data'] = request.POST

    else:
        form = AnkietaForm()

    context['text'] = napis
    context['instruktorostwo'] = list_instr
    context['form'] = form

    context['liczba_lat'] = liczba_lat
    context['foremnik'] = foremnik

    return render(request, 'basepage/ankieta.html', context)


def ocen_strone(request):
    if request.method == 'POST':
        form = OceniajStroneFORM(request.POST)
        if form.is_valid():
            form.save()

            return redirect('basepage:podziekowanie')


    else:
        form = OceniajStroneFORM()

    context = {
        'form': form,

        'liczba_lat': liczba_lat,
        'foremnik': foremnik,
    }
    return render(request, 'basepage/ocena_strony.html', context)


def odpowiedz_respondentowi(request):
    context = {
        'liczba_lat': liczba_lat,
        'foremnik': foremnik,
    }
    return render(request, 'basepage/ankieta_po.html', context)
