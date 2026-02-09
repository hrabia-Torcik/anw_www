from datetime import datetime
from datetime import date


teraz = datetime.now()
teraz_rok = teraz.strftime("%Y")
teraz_data = teraz.date()
# koniec_roku = datetime.date('2026','12','12')
koniec_roku = date(int(teraz_rok), 12, 31)

context = {}
list_pom = ['','','','','','']

if any(list_pom):
    print('kupa')

lis = ['cokolwiek', '', '', ' cokolwiek', '', '']

for i, ele in enumerate(lis):
    print(i)
    print(type(ele))


    if ele == '':
        ...
    else:
        if i == 0:
            print(ele)
            print('wlazlo')
            list_pom[0] = 'patent żeglarski'
            context['sub1'] = 'cokolwiek'
        if i == 1:
            print(ele)
            print('wlazlo')
            list_pom[1] = 'patent motorowodny'
            context['sub2'] = 'cokolwiek'
        if i == 2:
            print(ele)
            print('wlazlo')
            list_pom[2] = 'egzamin żeglarski'
            context['sub3'] = 'cokolwiek'
        if i == 3:
            print(ele)
            print('wlazlo')
            list_pom[3] = 'doszk'
            context['sub4'] = 'cokolwiek'
        if i == 4:
            print(ele)
            print('wlazlo')
            list_pom[4] = 'jachtowy sternik morski'
            context['sub5'] = 'cokolwiek'
        if i == 5:
            print(ele)
            print('wlazlo')
            list_pom[5] = 'lic'
            context['sub6'] = 'cokolwiek'
    print('*********************')
    print()
print(teraz)
print(teraz_rok)
print(teraz_data)
print(koniec_roku)
print()
print(list_pom)
print(context)

if any(list_pom):
    print('teraz niekupa')