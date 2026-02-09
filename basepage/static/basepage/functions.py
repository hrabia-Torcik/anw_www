import pandas as pd
import datetime
from basepage.models import *

categories = {'ŻJ':'patent żeglarski', 'JSM':'jachtowy sternik morski', 'PM':'patent motorowodny', 'LS':'licencja SRC','DŻ': 'doskonalenie żeglarskie','PNZ': 'podstawy nawigacji zliczeniowej','MJM': 'manewrowanie jachtem morskim','EŻ': 'egzamin żeglarski','EM': 'egzamin motorowodny'}
kursu_schedule_type = {'C':'codzienny', 'W':'łikendowy', 'J':'jednodniowy', 'DD':'dwudniowy'}

class Instructor():
    def __init__(self, instr_name, instr_surname, instr_email, instr_phone, instr_degree):
        self.__instr_name = instr_name
        self.__instr_surname = instr_surname
        self.__instr_email = instr_email
        self.__instr_phone = instr_phone
        self.__instr_degree = instr_degree

    def getInstr_name(self):
        return self.__instr_name

    def setInstr_name(self, h):
        self.__instr_name = h

    def getInstr_surname(self):
        return self.__instr_surname

    def setInstr_surname(self, h):
        self.__instr_name = h

    def getInstr_email(self):
        return self.__instr_email

    def setInstr_email(self, h):
        self.__instr_email = h

    def getInstr_phone(self):
        return self.__instr_phone

    def setInstr_phone(self, h):
        self.__instr_phone = h

    def getInstr_degree(self):
        return self.__instr_degree

    def setInstr_degree(self, h):
        self.__instr_degree = h

    def __str__(self):
        return f"Dane instruktora: {self.__instr_name} {self.__instr_surname}\n stopień instruktorski: {self.__instr_degree}, instruktoro_e-mail: {self.__instr_email}, telefon: {self.__instr_phone}"


class Participant():
    def __init__(self, p_uczestniko_name, p_uczestniko_surname, p_uczestniko_email, p_uczestniko_phone):
        self.__uczestniko_name = p_uczestniko_name
        self.__uczestniko_surname = p_uczestniko_surname
        self.__uczestniko_email = p_uczestniko_email
        self.__uczestniko_phone = p_uczestniko_phone


    def getUczestniko_name(self):
        return self.__uczestniko_name


    def setUczestniko_name(self, h):
        self.__uczestniko_name = h


    def getUczestniko_name(self):
        return self.__uczestniko_surname


    def setUczestniko_name(self, h):
        self.__uczestniko_surname = h


    def getUczestnikoo_email(self):
        return self.__uczestniko_email


    def setUczestniko_email(self, h):
        self.__uczestniko_email = h


    def getUczestniko_phone(self):
        return self.__uczestniko_phone


    def setUczestniko_phone(self, h):
        self.__uczestniko_phone = h


    def __str__(self):
        return f"Dane uczestnika: {self.__uczestniko_name} {self.__uczestniko_surname}\n e-uczestniko_e-mail: {self.__uczestniko_email}, telefon: {self.__uczestniko_phone}"


class ParticipantManager:
    def __init__(self):
        self.listParticipants = []

    def addParticipant (self,t,c,a,k):
        ktos = Participant(t,c,a,k)
        self.listParticipants.append(ktos)
        print("dodany")


    def showParticipants (self):
        for g in self.listParticipants:
            print(g) # Tutaj korzystam z metody STRING z klasy Participants
            # print(g.getImie(), g.getNazwisko()) # Tutaj natomiast wymieniam konkretne wartości.



    def delParticipant (self, par):
        for g in self.listParticipants:
            if (g.getNazwisko() == par):
                self.listParticipants.remove(g)
                print("Już go nie ma.")
                print("")


class Training(ParticipantManager):
    def __init__ (self,n,m,sched,date1,date2,kursu_prise):
        super().__init__()
        self.kursu_name = ''
        self.kursu_kodTraining = n
        self.category = m
        self.kursu_schedule = sched
        self.startDate = date1
        self.finishDate = date2
        self.kursu_prise = kursu_prise


    def menu(self):
        print(f"Witaj w kursie {self.kursu_kodTraining}")
        while(True):
            print(f"#### MENU kursu {self.kursu_kodTraining} ####")
            dec = input(" 1- dodaj kursanto, 2-pokaż listę kursantowstwa, 4-usuń kursanto z kursu, 5-koniec \n")

            if (dec == '1'):
                uczestniko_name = input("Podaj imię kursanto: ")
                uczestniko_surname = input("Podaj nazwisko kursanto: ")
                uczestniko_email = input("Podaj e-mail kursanto: ")
                uczestniko_phone = input("Podaj telefon kursanto: ")
                self.addParticipant(uczestniko_name, uczestniko_surname, uczestniko_email, uczestniko_phone)

            if (dec == '2'):

                self.showParticipants()


            if (dec == '4'):
                uczestniko_surname = input("Podaj nazwisko kursanto: ")
                self.delParticipant(uczestniko_surname)

            if (dec == '5'):
                break

    def __str__(self):
        return f"Dane kursu: {self.kursu_kodTraining} {self.category}\n uporządkowanie zajęć w czasie: {self.kursu_schedule}, data rozpoczęcia: {self.startDate}, data zakończenia: {self.finishDate}, cena: {self.kursu_prise} zł."


def dodaj_uczestU18(c: sqlite3.Cursor, uczestU18_name, uczestU18_surname, uczestU18_phone=None, uczestU18_email=None):

    sql = f'''
        INSERT INTO Uczest_under18 (uczestU18_name, uczestU18_surname, uczestU18_phone, uczestU18_email)
        VALUES (?, ?, ?, ?);
        '''

    c.execute(sql, (uczestU18_name, uczestU18_surname, uczestU18_phone, uczestU18_email ))

    return c.lastrowid, uczestU18_name, uczestU18_surname


def assign_U18_to_legalRepr(c: sqlite3.Cursor, opiek_lp, u18_lp):

    sql = f'''
        INSERT INTO przypis_Opiek_U18 (opiek_lp, u18_lp)
        VALUES (?, ?);
        '''

    c.execute(sql, (opiek_lp, u18_lp))

    return c.lastrowid, opiek_lp, u18_lp


def dodaj_uczestniko(c: sqlite3.Cursor, uczestniko_name, uczestniko_surname, uczestniko_phone, uczestniko_email):

    sql = f'''
        INSERT INTO Klientela (uczestniko_name, uczestniko_surname, uczestniko_phone, uczestniko_email)
        VALUES (?, ?, ?, ?);
        '''

    c.execute(sql, (uczestniko_name, uczestniko_surname, uczestniko_phone, uczestniko_email ))

    return c.lastrowid, uczestniko_name, uczestniko_surname


def dodaj_instruktoro(c: sqlite3.Cursor, instruktoro_name, instruktoro_surname, instruktoro_phone, instruktoro_email, instruktoro_degree):

    sql = f'''
        INSERT INTO Instruktorostwo (instruktoro_name, instruktoro_surname, instruktoro_phone, instruktoro_email, instruktoro_degree)
        VALUES (?, ?, ?, ?, ?);
        '''

    c.execute(sql, (instruktoro_name, instruktoro_surname, instruktoro_phone, instruktoro_email, instruktoro_degree ))

    return c.lastrowid, instruktoro_name, instruktoro_surname


def add_trainings_days(name, sched, d1, d2):

    print(d1)
    print(d2)
    d10 = datetime.date(int(d1[0:4]), int(d1[5:7]), int(d1[8:10]))
    d20 = datetime.date(int(d2[0:4]), int(d2[5:7]), int(d2[8:10]))
    step = d20 - d10
    print(step.days)
    if sched == kursu_schedule_type['C'] or sched == kursu_schedule_type['W']:
        control_day = datetime.date(int(d1[0:4]), int(d1[5:7]), int(d1[8:10])).isoweekday()
        if str(control_day) == '6':
            wydr = 'Okej, jest sobota'
        else:
            wydr = 'O, nie! To jakiś inny dzień.'
        print(wydr)
    if sched == kursu_schedule_type['J'] or sched == kursu_schedule_type['DD'] or sched == kursu_schedule_type['C']:

        nr = int(step.days) - 1
        put_it = [str(d20)]
        for _ in range(int(step.days)):
            el = d10 + datetime.timedelta(days=nr)
            put_it.insert(0,str(el))
            nr += -1
            print(el)

    elif sched == kursu_schedule_type['W']:
        dzielnik = int(step.days) % 7
        print(int(round(((int(step.days)-dzielnik)/7),0)))
        nr = 0
        put_it = []
        for _ in range(int(round(((int(step.days)-dzielnik)/7),0))+1):
            el = d10 + datetime.timedelta(days=nr)
            put_it.append(str(el))
            el = d10 + datetime.timedelta(days=nr + 1)
            put_it.append(str(el))
            nr += 7

    conn = sqlite3.connect(bazaD)
    c = conn.cursor()

    # conn.commit()
    # conn.close()
    sql = f'''
                    SELECT kursu_lp FROM Kursy_wszystkie
                    WHERE kursu_kod = ?;
                    '''

    c.execute(sql, (name,))
    kursu_id0 = c.fetchone()
    conn.close()

    kursu_id = kursu_id0[0]

    conn = sqlite3.connect(bazaD)
    c = conn.cursor()
    for elem in put_it:


        sql = f'''
            INSERT OR IGNORE INTO Dni_kursowe (data_dnia)
            VALUES (?);
            '''

        c.execute(sql, (elem,))

        last_id = c.lastrowid
        conn.commit()
    conn.close()

    conn = sqlite3.connect(bazaD)
    c = conn.cursor()



    for elem in put_it:
        sql = f'''
                                SELECT dnia_lp FROM Dni_kursowe
                                WHERE data_dnia = ?;
                                '''

        c.execute(sql, (elem,))
        dnia_id0 = c.fetchone()
        assign_Instructor_or_Training_to_day(c, dnia_id0[0], kursu_lp=kursu_id)
        conn.commit()
    conn.close()

    return put_it


def nameKursu_assign(kod):

    korek = ''.join([el for el in kod if el.isdigit() is False and el != '/' and el.isupper() is True])

    return categories[korek]

def dodaj_Kurs(c: sqlite3.Cursor, kursu_kod, kursu_schedule, kursu_data_start, kursu_data_end, kursu_prise):


    dla_kursu_name = nameKursu_assign(kursu_kod)

    sql = f'''
        INSERT INTO Kursy_wszystkie (kursu_name, kursu_kod, kursu_schedule, kursu_data_start, kursu_data_end, kursu_prise)
        VALUES (?, ?, ?, ?, ?, ?);
        '''

    c.execute(sql, (dla_kursu_name, kursu_kod, kursu_schedule, kursu_data_start, kursu_data_end, kursu_prise))

    return c.lastrowid, kursu_kod, kursu_data_start, kursu_data_end

def del_Kurs(c: sqlite3.Cursor, kursu_lp):

    sql = f'''
        DELETE FROM Kursy_wszystkie
        WHERE kursu_lp = ?;
        '''

    c.execute(sql, (kursu_lp,))

    return c.lastrowid


def assign_Instructor_or_Training_to_day(c: sqlite3.Cursor, dnia_kursu_lp, inst_lp=None, kursu_lp=None):

    print('Robi dodanie kursu lub instruktora dla dnia: ', dnia_kursu_lp, " dotyczy kursu o nr lp: ", kursu_lp, ' instruktora lp: ', inst_lp )

    if inst_lp and kursu_lp:
        sql = '''
                SELECT dnia_kursu_lp, inst_lp FROM przypisanie_do_dnia_Kursu WHERE inst_lp=? and dnia_kursu_lp=?;
                '''
        c.execute(sql, (inst_lp, dnia_kursu_lp))
        kolec = c.fetchall()

        if len(kolec) != 0:
            print()
            flare = input('Słuchaj, ten instruktor już pracuje w tym dniu... Na pewno go dopisywać? Wpisz t lub n.')
        else:
            flare = 1
        if flare == 1:
            sql = f'''
                INSERT INTO przypisanie_do_dnia_Kursu (dnia_kursu_lp, inst_lp)
                VALUES (?, ?);
                '''
            c.execute(sql, (dnia_kursu_lp, inst_lp))



    if kursu_lp and inst_lp is None:
        sql = f'''
            INSERT INTO przypisanie_do_dnia_Kursu (dnia_kursu_lp, od_kursu_lp)
            VALUES (?, ?);
            '''
        c.execute(sql, (dnia_kursu_lp, kursu_lp))

    return c.lastrowid, dnia_kursu_lp, inst_lp, kursu_lp


def dodaj_zapis_na_Kurs(c: sqlite3.Cursor, krs_lp, data_zapisu_nakrs, uczest_lp=None, uczU18_lp=None, instruk_lp=None):

    if instruk_lp:
        sql = f'''
            INSERT INTO zapisy_na_Kursy (instruk_lp, krs_lp, data_zapisu_nakrs)
            VALUES (?, ?, ?);
            '''

        c.execute(sql, (instruk_lp, krs_lp, data_zapisu_nakrs))

    if uczest_lp:
        sql = f'''
            INSERT INTO zapisy_na_Kursy (uczest_lp, krs_lp, data_zapisu_nakrs)
            VALUES (?, ?, ?);
            '''

        c.execute(sql, (uczest_lp, krs_lp, data_zapisu_nakrs))

    if uczU18_lp:
        sql = f'''
            INSERT INTO zapisy_na_Kursy (uczU18_lp, krs_lp, data_zapisu_nakrs)
            VALUES (?, ?, ?);
            '''

        c.execute(sql, (uczU18_lp, krs_lp, data_zapisu_nakrs))

    return c.lastrowid, instruk_lp, uczest_lp, uczU18_lp, krs_lp, data_zapisu_nakrs

def edytuj_kurs(c: sqlite3.Cursor, changeWhat, changeValue, whos):
    # print('EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
    flaga = 0
    if changeWhat == 'kursu_kod':
        print('AAAAAAAAA        wlazło tu')
        flaga = 1
        sql = f'''
        UPDATE
          Kursy_wszystkie
        SET
          'kursu_kod' = ?
    
        WHERE kursu_lp = ?;
        '''
        kucyk = ''
        if changeValue.count('c') == 1:
            kucyk = kursu_schedule_type['C']
        elif changeValue.count('w') == 1:
            kucyk = kursu_schedule_type['W']
        if kucyk:
            print('tak, było oznaczenie typu harmonogramu.')
            sql2 = f'''
                        SELECT kursu_schedule FROM Kursy_wszystkie
                        
                        WHERE kursu_lp = ?;
                        '''
            c.execute(sql2, (whos,))
            check2 = c.fetchall()
            if check2[0][0] != kucyk:
                if kucyk == kursu_schedule_type['C']:
                    coniun = 'codziennego'
                elif kucyk == kursu_schedule_type['W']:
                    coniun = 'łikendowego'
                print(f'Hej, coś się nie zgadza! Wprowadziłaś oznaczenie dla kursu {coniun}, a z dat wynika co innego.\nSprawdź daty kursu.')
                input('Naciśnij cokolwiek.')
            else:
                print('Jest zgodne z tym, co wynika z dat.')


    elif changeWhat == 'kursu_schedule':
        sql = f'''
                        UPDATE
                          Kursy_wszystkie
                        SET
                          'kursu_schedule' = ?

                        WHERE kursu_lp = ?;
                        '''
    elif changeWhat == 'kursu_data_start':
        sql = f'''
                UPDATE
                  Kursy_wszystkie
                SET
                  'kursu_data_start' = ?

                WHERE kursu_lp = ?;
                '''
    elif changeWhat == 'kursu_data_end':
        sql = f'''
                UPDATE
                  Kursy_wszystkie
                SET
                  'kursu_data_end' = ?

                WHERE kursu_lp = ?;
                '''
    elif changeWhat == 'kursu_prise':
        sql = f'''
                UPDATE
                  Kursy_wszystkie
                SET
                  'kursu_prise' = ?

                WHERE kursu_lp = ?;
                '''
    c.execute(sql, (changeValue, whos))

    if flaga == 1:
        dla_kursu_name = nameKursu_assign(changeValue)
        sql = f'''
                        UPDATE
                          Kursy_wszystkie
                        SET
                          'kursu_name' = ?

                        WHERE kursu_lp = ?;
                        '''
        c.execute(sql, (dla_kursu_name, whos))

    # if changeWhat == 'kursu_data_start' or changeWhat == 'kursu_data_end':
    #     ...

    # print("end_____end_____end_____end_____end_____end_____end_____end")
    return whos, changeWhat, changeValue


def find_schedule_type(data1,data2):
    roznica = str(data2 - data1)
    # print(roznica)
    if roznica[0] == '0':
        sched_char = kursu_schedule_type['J']
    else:
        roznica_nonZero = int(roznica.split(' ')[0])
        if roznica_nonZero == 1:
            sched_char = kursu_schedule_type['DD']
        elif 0 < roznica_nonZero <= 8:
            sched_char = kursu_schedule_type['C']
        elif 8 < roznica_nonZero < 30:
            sched_char = kursu_schedule_type['W']
        else:
            print('Wprowadzono bzdurne daty.')
            sched_char = 'bzdurne daty'

    return sched_char



def display_all_trainings(datas):

    kolec = get_trainings_from_base(datas)
    for el in kolec:
        symbol = ''.join([el for el in el[1] if el.isupper()])
        print(f"{categories[symbol]:32} {el}")


def analize_data_from_xlsx(plik):

    trainingsChanges = {'trainings to edit':[], 'trainings to delete':[], 'trainings to add':[]}

    kot = KursyWszystkie.objects.all()

    listTrainingsFromBase = []

    for el in kot:
        listTrainingsFromBase.append((el.kursu_lp, el.kursu_kod, el.kursu_schedule, el.kursu_data_start, el.kursu_data_end,
                           el.kursu_prise, el.kursu_name))


    tabDF = pd.read_excel(plik, index_col=0)

    list_keys = [el for el in tabDF]
    row, columns = tabDF.shape
    listTrainingsFromXlsx = []
    for el in list(range(row)):
        insert_data = dict(tabDF.iloc[el])
        kursu_data_start = insert_data[list_keys[1]].date()
        if str(insert_data[list_keys[2]]) == 'NaT':
            kursu_data_end = kursu_data_start
        else:
            kursu_data_end = insert_data[list_keys[2]].date()
        sched_char = find_schedule_type(kursu_data_start,kursu_data_end)

        symbol = ''.join([el for el in insert_data[list_keys[0]] if el.isupper()])
        listTrainingsFromXlsx.append(KursyWszystkie(insert_data[list_keys[0]], categories[symbol],
                                              sched_char, str(kursu_data_start), str(kursu_data_end),
                                              int(insert_data[list_keys[3]])))
    #
    # new_trainings_objects = []
    # for somet in listTrainingsFromXlsx:
    #     fl = 0
    #
    #
    #     for ink in listTrainingsFromBase:
    #         if somet.kursu_kodTraining == ink[1]:
    #             fl = 1
    #     if fl == 0:
    #         new_trainings_objects.append(somet)
    #
    # counter = 0
    # for el in listTrainingsFromBase:
    #     counter += 1
    #     print(counter)
    #     print(el)
    #     flaga1 = 0
    #     flaga333 = 0
    #     for something in listTrainingsFromXlsx:
    #         # print(something.kursu_kodTraining, len(something.kursu_kodTraining))
    #         if el[1] == something.kursu_kodTraining:
    #             flaga333 = 1
    #
    #             if el[3] != something.startDate:
    #                 print('data1 inna')
    #                 trainingsChanges['trainings to edit'].append(['kursu_data_start', something.startDate, el[0]])
    #                 flaga1 = 1
    #             if el[4] != something.finishDate:
    #                 print('data2 inna')
    #                 trainingsChanges['trainings to edit'].append(['kursu_data_end', something.finishDate, el[0]])
    #                 flaga1 = 1
    #             if el[5] != something.kursu_prise:
    #                 print('cena inna')
    #                 trainingsChanges['trainings to edit'].append(['kursu_prise', int(something.kursu_prise), el[0]])
    #                 flaga1 = 1
    #             if flaga1 == 0:
    #                 print('Nie ma żadnych zmian, niczego nie robię.')
    #
    #     if flaga333 == 0:
    #         flare = 0
    #         for rel in new_trainings_objects:
    #             if rel.startDate == el[3] and rel.finishDate == el[4] and rel.kursu_prise == el[5]:
    #                 flare = 1
    #                 print('Wśród nowych kursów znalazłam taki, co ma dokładnie takie same charakterystyki.')
    #                 decis = input(f'Czy chcesz zmienić nazwę na {rel.kursu_kodTraining}? wpisz t lub n: ')
    #                 if decis == 't':
    #                     trainingsChanges['trainings to edit'].append(['kursu_kod', rel.kursu_kodTraining, el[0]])
    #                     new_trainings_objects.remove(rel)
    #
    #         if flare == 0:
    #             print('Dla tego kursu:',el)
    #             print('Nie za bardzo widać odpowiednik wśród nowych kursów.')
    #             klep = input('Czyżbyś chciała go usunąć? Wpisz t lub n: ')
    #             if klep == 't':
    #                 trainingsChanges['trainings to delete'].append(str(el[0]))
    #
    #     print('"""""""""""""""""""""""""""""""""')
    #     print()
    #
    # for tret in new_trainings_objects:
    #     print(tret)
    #     trainingsChanges['trainings to add'].append([tret.kursu_kodTraining, tret.kursu_schedule, tret.startDate, tret.finishDate, tret.kursu_prise])


    return trainingsChanges


def implementChanges(database, to_change):

    for elee in to_change:

        list_to_check = []
        if to_change[elee]:
            print(f"{elee}:")
            print(to_change[elee])
            for tyk in to_change[elee]:
                flare1 = 0
                if elee == 'trainings to add':
                    print('dodam')
                    conn = sqlite3.connect(database)
                    c = conn.cursor()
                    dodaj_Kurs(c, tyk[0], tyk[1], tyk[2], tyk[3], tyk[4])
                    conn.commit()
                    conn.close()

                    ######  tu musi się odpalić funkcja dodawania dni
                    add_trainings_days(tyk[0], tyk[1], tyk[2], tyk[3])
                    # conn.commit()

                elif elee == 'trainings to edit':
                    print('edytuję')
                    conn = sqlite3.connect(database)
                    c = conn.cursor()
                    checksched = edytuj_kurs(c, tyk[0], tyk[1], tyk[2])
                    conn.commit()
                    conn.close()
                    print(checksched)
                    if checksched[1] == 'kursu_data_start' or checksched[1] == 'kursu_data_end':
                        flare1 = 1
                elif elee == 'trainings to delete':
                    print('usunę')
                    del_Kurs(c, tyk)

                if flare1 == 1:
                    print('Sprawdza się poprawność nowej nazwy.')
                    conn = sqlite3.connect(database)
                    c = conn.cursor()

                    sql = '''
                                            SELECT * FROM Kursy_wszystkie
                                            WHERE kursu_lp = ?;
                                            '''

                    c.execute(sql, (checksched[0],))
                    dane = c.fetchall()[0]
                    conn.close()
                    # print(dane)
                    d1 = dane[3].split('-')
                    d2 = dane[4].split('-')
                    # print(d1, d2)

                    data1 = datetime.datetime(int(d1[0]), int(d1[1]), int(d1[2]))
                    data2 = datetime.datetime(int(d2[0]), int(d2[1]), int(d2[2]))

                    schedchar = find_schedule_type(data1, data2)

                    list_to_check.append(('kursu_schedule', schedchar, dane[0]))



        if len(list_to_check) > 0:
            conn = sqlite3.connect(bazaD)
            c = conn.cursor()
            for el in list_to_check:
                edytuj_kurs(c, el[0], el[1], el[2])
            conn.commit()
            conn.close()


def display_some_training(c: sqlite3.Cursor, kursu_lp):

    desc_training = kursu_lp
    desc_training = str(desc_training)
    sql = '''
                    SELECT uczestniko_lp, uczestniko_name, uczestniko_surname, uczestniko_phone, uczestniko_email,
                    kursu_kod, kursu_schedule, kursu_data_start, kursu_data_end, kursu_prise
                    FROM Klientela join zapisy_na_Kursy ON uczestniko_lp=uczest_lp and krs_lp like ? join Kursy_wszystkie ON krs_lp=kursu_lp;
                    '''

    c.execute(sql, (desc_training,))
    kolec1 = c.fetchall()
    sql = '''
                    SELECT uczestU18_lp, uczestU18_name, uczestU18_surname, uczestU18_phone, uczestU18_email,
                    kursu_kod, kursu_schedule, kursu_data_start, kursu_data_end, kursu_prise
                    FROM Uczest_under18
                    join zapisy_na_Kursy ON uczestU18_lp=uczU18_lp and krs_lp like ?
                    join Kursy_wszystkie ON krs_lp=kursu_lp
                    join przypis_Opiek_U18 ON u18_lp=uczestU18_lp
                    join Klientela ON opiek_lp=uczestniko_lp;
                    '''

    c.execute(sql, (desc_training,))
    kolec2 = c.fetchall()
    kolec3 = []

    for rel in kolec2:
        uczU18_lp = str(rel[0])
        sql = '''
                    SELECT uczestU18_lp, uczestU18_name, uczestU18_surname, uczestniko_name, uczestniko_surname, uczestniko_phone, uczestniko_email
                    FROM Uczest_under18
                    join przypis_Opiek_U18 ON u18_lp=uczestU18_lp and u18_lp like ?
                    join Klientela ON opiek_lp=uczestniko_lp;
                    '''

        c.execute(sql, (uczU18_lp,))

        kotlec = c.fetchall()
        kolec3.append(kotlec)

    kolec22 = []
    for el in kolec2:
        if el not in kolec22:
            kolec22.append(el)
    kolec33 = []
    for el in kolec3:
        if el not in kolec33:
            kolec33.append(el)
    kolec4 = []
    for i, j in enumerate(kolec22):
        trel = [otr for otr in j]
        trel2 = {}
        nr = 0
        for klep in kolec33[i]:
            nr += 1
            descr = "representant" + str(nr)
            trel2[descr] = klep[3:]
        trel.append(trel2)
        kolec4.append(tuple(trel))

    kolecost2 = kolec1 + kolec4
    nrRo = 0
    korek = ''.join([el for el in kolecost2[0][5] if el.isdigit() is False and el != '/' and el.isupper() is True])

    for el in kolecost2:
        nrRo += 1
        if nrRo == 1:
            print(
                f"To są uczestnicy kursu {categories[korek]}, symbol {el[5]}, odbywający się od {el[7]} do {el[8]}, tryb zajęć {el[6]}, cena {el[9]} zł:")
        to_print = f'{str(el[0]):>7}, {str(el[1])} {str(el[2])}, {str(el[3])}, {str(el[4])}'
        if len(el) > 10:
            to_print = to_print + ', reprezentowana/ny przez: '
            krs = 0
            for ret in el[10]:
                krs += 1
                if len(el[10]) == 1:
                    okre = ''
                else:
                    okre = ret + ' -> '
                par0 = ", ".join(el[10][ret])
                par = ''
                kla = 0
                for klr in par0:
                    if klr == ',' and kla == 0:
                        kla = 1
                    else:
                        par += klr
                if krs < 2:
                    to_print = to_print + okre + par
                else:
                    to_print = to_print + '; ' + okre + par
            to_print = f"{to_print}"
        print(to_print)

    return kolecost2


def find_person_lp_by_data(nap):

    for _ in range(2):
        napROB = nap
        nr = 0
        mnr = 0
        monkey = 0
        lengthNap = len(napROB)
        for el in napROB:
            if el.isdigit():
                nr += 1
            if el.isdigit() or el == ' ':
                mnr += 1
            if el == '@':
                monkey = 1

        if nr >= 7 and (0 <= lengthNap-mnr <= 1) and monkey == 0:
            napROB.strip()
            tryk = napROB.replace(' ','')
            list3 = [el + '%' for el in tryk]
            nap0 = ''.join(list3)
            napROB = nap0

        conn = sqlite3.connect(bazaD)
        c = conn.cursor()

        sql = '''
                            SELECT * FROM Klientela
                            WHERE uczestniko_name=? or uczestniko_surname=? or uczestniko_phone like ? or uczestniko_email=? 
                            ;
                            '''
        c.execute(sql, (napROB, napROB, napROB, napROB))
        jerko1 = c.fetchall()
        jerko = [el for el in jerko1]


        sql = '''
                                    SELECT * FROM Uczest_under18
                                    WHERE uczestU18_name=? or uczestU18_surname=? or uczestU18_phone like ? or uczestU18_email=? 
                                    ;
                                    '''
        c.execute(sql, (napROB, napROB, napROB, napROB))
        jerko22 = c.fetchall()
        conn.commit()
        conn.close()

        if len(jerko22) > 0:
            for el in jerko22:
                rob = [el1 for el1 in el]
                rob.append('ta osoba była na kursie jako małoletnia')
                jerko.append(tuple(rob))


        if len(jerko) == 0 and lengthNap == mnr:
            nap = '+48' + nap
        else:
            break

    return jerko


def looking_for_person(list):

    list_catches = []
    conn = sqlite3.connect(bazaD)
    c = conn.cursor()
    for ele in list:
        dict = {'numer': ele}
        nrUser = str(ele)
        sql = '''
                    SELECT uczestniko_lp, uczestniko_name, uczestniko_surname, uczestniko_phone, uczestniko_email,
                    kursu_kod, kursu_schedule, kursu_data_start, kursu_data_end, kursu_prise
                    FROM Klientela
                    join zapisy_na_Kursy ON uczestniko_lp=uczest_lp and uczestniko_lp like ?
                    join Kursy_wszystkie ON krs_lp=kursu_lp;
                    '''
        c.execute(sql, (nrUser,))
        jerko = c.fetchall()
        dict['kursy pełnoletnich'] = jerko

        sql = '''
                    SELECT uczestniko_lp, uczestniko_name, uczestniko_surname, uczestniko_phone, uczestniko_email,
                    uczestU18_lp, uczestU18_name, uczestU18_surname, uczestU18_phone, uczestU18_email, kursu_kod,
                    kursu_schedule, kursu_data_start, kursu_data_end, kursu_prise
                    FROM Klientela
                    join przypis_Opiek_U18 ON uczestniko_lp=opiek_lp and uczestniko_lp like ?
                    join Uczest_under18 ON u18_lp=uczestU18_lp
                    join zapisy_na_kursy ON u18_lp=uczU18_lp
                    join Kursy_wszystkie ON krs_lp=kursu_lp;
                    '''

        c.execute(sql, (nrUser,))
        jerko = c.fetchall()
        dict['kursy małoletnich'] = jerko
        list_catches.append(dict)
    conn.commit()
    conn.close()
    flage = 0
    print()
    for el in list_catches:
        melo_flare = 0
        if len(el['kursy pełnoletnich']) > 0:
            for i, j in enumerate(el['kursy pełnoletnich']):
                if i == 0:
                    print(
                        f'{j[1]} {j[2]} (numer w bazie:{j[0]}, tel.: {j[3]}, e-mail: {j[4]}) było/jest na takich kursach:')
                list = [str(el) for el in j[5:]]
                oset = list[-1]
                list[-1] = oset + ' zł'
                korek = ''.join([el for el in list[0] if el.isdigit() is False and el != '/' and el.isupper() is True])
                print(f"     {categories[korek]:32} {', '.join(list)}")
            flage = 1
            melo_flare = 1
        if len(el['kursy małoletnich']) > 0:
            for i, j in enumerate(el['kursy małoletnich']):
                insertion1 = 'swoją/ego podopieczną/ego'
                if len(el['kursy małoletnich']) < 2:
                    insertion2 = 'taki kurs'
                else:
                    insertion2 = 'takie kursy'
                if len(el['kursy małoletnich']) >= 2:
                    flagre = 0
                    temp0 = ''
                    for eli in el['kursy małoletnich']:
                        temp = eli[6] + ' ' + eli[7]
                        if temp != temp0 and temp0 != '':
                            flagre = 1
                        temp0 = temp
                    if flagre == 1:
                        insertion1 = 'swoich podopiecznych'

                if i == 0:
                    print(
                        f'{j[1]} {j[2]} (numer w bazie:{j[0]}, tel.: {j[3]}, e-mail: {j[4]}) zapisała/ał {insertion1} na {insertion2}:')
                list = [str(el) for el in j[5:]]
                oset = list[-1]
                list[-1] = oset + ' zł'
                korek = ''.join([el for el in list[5] if el.isdigit() is False and el != '/' and el.isupper() is True])
                if list[3] != 'None':
                    insertion3 = f" (tel.: {list[3]}) "
                    if list[4] != 'None':
                        insertion3 = insertion3[:-2] + ', e-mail: ' + list[4] + ')'
                elif list[4] != 'None':
                    insertion3 = f" (e-mail: {list[4]}) "
                else:
                    insertion3 = ''

                print(
                    f"     {list[1]} {list[2]}{insertion3} chodziła/ił na:\n           {categories[korek]:32} {', '.join(list[5:])}")
            flage = 1
            melo_flare = 1
        if melo_flare == 0:
            print(
                f"Osoba o podanych danych (numer w bazie: {el['numer']}) nie zapisała ani siebie, ani nikogo innego na jakikolwiek kurs.")
        print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        print()
    if flage == 0:
        print('Nikogo o takich danych nie znalazłam... Przykro mi :/')

    return list_catches


if __name__ == '__main__':

    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    #
    # sql = '''
    #     DROP TABLE Kursy_wszystkie;
    #     '''
    #
    # c.execute(sql)
    #
    # conn.commit()
    # conn.close()

    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    #
    # sql = '''
    #     CREATE TABLE Dni_kursowe (
    #         dnia_lp INTEGER PRIMARY KEY NOT NULL,
    #         data_dnia DATE UNIQUE
    #     );
    #
    #     '''
    #
    # c.execute(sql)
    #
    # conn.commit()
    # conn.close()
    #
    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    # sql = '''
    #     CREATE TABLE przypisanie_do_dnia_Kursu (
    #         przypisanie_Instr_lp INTEGER PRIMARY KEY NOT NULL,
    #         dnia_kursu_lp INT(5),
    #         inst_lp INT(5),
    #         od_kursu_lp INT(5),
    #         FOREIGN KEY (dnia_kursu_lp) REFERENCES Dni_kursowe(dnia_lp),
    #         FOREIGN KEY (inst_lp) REFERENCES Instruktorostwo(instruktoro_lp),
    #         FOREIGN KEY (od_kursu_lp) REFERENCES Kursy_wszystkie(kursu_lp)
    #     );
    #
    #     '''
    #
    # c.execute(sql)
    # conn.commit()
    # conn.close()


    ##############################################  Zmiana nazwy kolumny w określonej tabeli
    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    #
    # sql = '''
    # ALTER TABLE zapisy_na_Kursy
    # RENAME COLUMN uczU18_lp1111 TO uczU18_lp;
    # '''
    # c.execute(sql)
    # conn.commit()
    # conn.close()
    ...

    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    #
    # sql = '''
    #     UPDATE Klientela
    #     SET uczestniko_phone = '632985417'
    #     WHERE uczestniko_lp = 13;
    #     '''
    #
    # c.execute(sql)
    #
    # conn.commit()
    # conn.close()
    ...

    #################          Dodanie nowej kolumny

    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    #
    # sql = '''
    #         ALTER TABLE zapisy_na_Kursy
    #         ADD COLUMN uczU18_lp INT(5);
    #
    #         '''
    #
    # c.execute(sql)
    # conn.commit()
    # conn.close()

    #######################################################################################
    ...
    ##############               Tutaj jest sprytne skopiowanie danych z tabeli, którą później usuniemy,
    ##############               by stworzyć ją na nowo z nową kolumną (tutaj "uczU18_lp") oraz konieczną
    ##############               do niej nową definicją klucza obcego

    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    #
    #
    # sql = '''
    # CREATE TEMPORARY TABLE temp
    # AS SELECT * FROM zapisy_na_Kursy;
    # '''
    # c.execute(sql)

    # sql = '''
    # DROP TABLE zapisy_na_Kursy;
    # '''
    # c.execute(sql)
    #
    # sql = '''
    # CREATE TABLE zapisy_na_Kursy(
    #     zapisu_lp INTEGER,
    #     uczest_lp INT,
    #     krs_lp INT,
    #     uczU18_lp INT,
    #     instruk_lp INT,
    #     data_zapisu_nakrs DATE,
    #     PRIMARY KEY(zapisu_lp),
    #     FOREIGN KEY(uczest_lp) REFERENCES Klientela(uczestniko_lp),
    #     FOREIGN KEY(krs_lp) REFERENCES Kursy_wszystkie(kursu_lp),
    #     FOREIGN KEY(uczU18_lp) REFERENCES Uczest_under18(uczestU18_lp)
    #     FOREIGN KEY(instruk_lp) REFERENCES Instruktorostwo(instruktoro_lp)
    # );
    # '''
    # c.execute(sql)
    #
    # sql = '''
    # INSERT INTO zapisy_na_Kursy SELECT * FROM temp;
    # '''
    # c.execute(sql)

    # sql = '''
    # DROP
    # TABLE
    # temp;
    # '''

    # c.execute(sql)
    #
    # conn.commit()
    # conn.close()
    #################################################################################################################
    #################################################################################################################


    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    # sql = '''
    #     CREATE TABLE przypis_Opiek_U18 (
    #         przypisuOU18_lp INTEGER PRIMARY KEY NOT NULL,
    #         opiek_lp INT(5),
    #         u18_lp INT(5),
    #         FOREIGN KEY (opiek_lp) REFERENCES Klientela(uczestniko_lp),
    #         FOREIGN KEY (u18_lp) REFERENCES Uczest_under18(uczestU18_lp)
    #     );
    #
    #     '''
    #
    # c.execute(sql)
    # conn.commit()
    # conn.close()

    #
    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    #
    # sql = '''
    # CREATE TABLE Instruktorostwo (
    #     instruktoro_lp INTEGER NOT NULL,
    #     instruktoro_name VARCHAR(25),
    #     instruktoro_surname VARCHAR(80),
    #     instruktoro_phone INT(15) NOT NULL,
    #     instruktoro_email VARCHAR(125) NOT NULL,
    #     instruktoro_degree VARCHAR(45) NOT NULL,
    #     PRIMARY KEY (instruktoro_lp)
    # );
    # '''
    #
    # c.execute(sql)
    #
    # conn.commit()
    # conn.close()
    #
    #
    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    # sql = '''
    # CREATE TABLE Kursy_wszystkie (
    #     kursu_lp INTEGER NOT NULL,
    #     kursu_kod VARCHAR(25) UNIQUE,
    #     kursu_schedule VARCHAR(25),
    #     kursu_data_start DATE,
    #     kursu_data_end DATE,
    #     kursu_prise INT,
    #     PRIMARY KEY (kursu_lp)
    # );
    #
    # '''
    #
    # c.execute(sql)
    # conn.commit()
    # conn.close()
    #
    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    # sql = '''
    #     CREATE TABLE zapisy_na_Kursy (
    #         zapisu_lp INTEGER PRIMARY KEY NOT NULL,
    #         uczest_lp INT(5),
    #         krs_lp INT(5),
    #         data_zapisu_nakrs DATE,
    #         FOREIGN KEY (uczest_lp) REFERENCES Klientela(uczestniko_lp),
    #         FOREIGN KEY (krs_lp) REFERENCES Kursy_wszystkie(kursu_lp)
    #     );
    #
    #     '''
    #
    # c.execute(sql)
    # conn.commit()
    # conn.close()

    ...

    # for _ in range(5):
    #     conn = sqlite3.connect(bazaD)
    #     c = conn.cursor()
    #     f = Faker('PL_pl')
    #     dodaj_uczestU18(c, f.first_name(), f.last_name(), f.phone_number(), f.email())
    #     conn.commit()
    #     conn.close()
    #
    # for _ in range(3):
    #     conn = sqlite3.connect(bazaD)
    #     c = conn.cursor()
    #     f = Faker('PL_pl')
    #     dodaj_uczestU18(c, f.first_name(), f.last_name())
    #     conn.commit()
    #     conn.close()


    ########################     Usunięcie rekordów z danej tabeli:
    ##############                Jeśli nie ma parametru WHERE, to usuną się wszystkie rekordy

    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    #
    # sql = f'''
    #     DELETE FROM Kursy_wszystkie
    #     WHERE kursu_lp>20
    #     ;
    #     '''
    #
    # c.execute(sql)
    #
    # conn.commit()
    # conn.close()
    ...
    ##############################################################################################################

    to_change = analize_data_from_xlsx(bazaD, "anw-kursy-out22.xlsx")
    if to_change['trainings to edit'] or to_change['trainings to delete'] or to_change['trainings to add']:
        implementChanges(bazaD, to_change)


    print()
    display_all_trainings(bazaD)

    ###############################################################################################################
    ...
    # f = Faker('PL_pl')
    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    #
    #
    # dodaj_zapis_na_Kurs(c, 4, f.date(), uczest_lp=9)
    # dodaj_zapis_na_Kurs(c, 4, f.date(), uczest_lp=10)
    # dodaj_zapis_na_Kurs(c, 4, f.date(), uczest_lp=1)
    # dodaj_zapis_na_Kurs(c, 14, f.date(), uczest_lp=9)
    # dodaj_zapis_na_Kurs(c, 8, f.date(), uczest_lp=4)
    #
    # dodaj_zapis_na_Kurs(c, 4, f.date(), uczU18_lp=1)
    # dodaj_zapis_na_Kurs(c, 15, f.date(), uczU18_lp=8)
    # dodaj_zapis_na_Kurs(c, 8, f.date(), uczU18_lp=6)
    # dodaj_zapis_na_Kurs(c, 15, f.date(), uczU18_lp=6)
    #
    # conn.commit()
    # conn.close()

    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    #
    #
    # assign_U18_to_legalRepr(c, 6, 1)
    # assign_U18_to_legalRepr(c, 6, 2)
    # assign_U18_to_legalRepr(c, 11, 3)
    # assign_U18_to_legalRepr(c, 5, 4)
    # assign_U18_to_legalRepr(c, 9, 4)
    # assign_U18_to_legalRepr(c, 1, 5)
    # assign_U18_to_legalRepr(c, 17, 6)
    # assign_U18_to_legalRepr(c, 13, 7)
    # assign_U18_to_legalRepr(c, 10, 8)
    #
    # conn.commit()
    # conn.close()


    ...

    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()

    # dodaj_instruktoro(c, 'Maciej', 'Oporski', '501010386', 'maciej@example.net', 'MIŻ')
    # dodaj_instruktoro(c, 'Maciej', 'Fidecki', '724699413', 'maciejmalarski@example.net', 'IŻ')
    # dodaj_instruktoro(c, 'Ola', 'Topolska', '668472244', 'olatop@example.net', 'MIŻ')
    # dodaj_instruktoro(c, 'Basza', 'Biczel', '784569678', 'baszb@example.net', 'NŻ')

    # conn.commit()
    # conn.close()

    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    #
    #
    # for ter in [29]:
    #     datas_add = assign_Instructor_or_Training_to_day(c, str(ter) ,inst_lp='1', kursu_lp=14)
    #
    # conn.commit()
    # conn.close()
    #
    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    #
    # sql = '''
    #     SELECT krs_lp, instruk_lp FROM zapisy_na_Kursy WHERE instruk_lp=? and krs_lp=?;
    #     '''
    # c.execute(sql, (datas_add[2], datas_add[3]))
    # kolec = c.fetchall()
    # print(kolec)
    # conn.close()
    # if len(kolec) == 0:
    #     date_zapisu = datetime.datetime.now()
    #     date_zapisu = str(date_zapisu.date())
    #     conn = sqlite3.connect(bazaD)
    #     c = conn.cursor()
    #     dodaj_zapis_na_Kurs(c, datas_add[3], date_zapisu, instruk_lp=datas_add[2])
    #     conn.commit()
    #     conn.close()

    # for ter in range(2):
    #     assign_Instructor_or_Training_to_day(c, str(ter+45) ,inst_lp='2', kursu_lp=None)
    #
    # for ter in range(8):
    #     assign_Instructor_or_Training_to_day(c, str(ter+30) ,inst_lp='3', kursu_lp=None)
    #
    # for ter in range(6):
    #     assign_Instructor_or_Training_to_day(c, str(ter+12) ,inst_lp='2', kursu_lp=None)
    #
    # for ter in range(6):
    #     assign_Instructor_or_Training_to_day(c, str(ter+12) ,inst_lp='4', kursu_lp=None)
    #
    # for ter in range(8):
    #     assign_Instructor_or_Training_to_day(c, ter+30 ,inst_lp=4, kursu_lp=None)



    ...
    #######################################################

    ############
    #### USUNIĘCIE TABELI

    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    #
    # sql = '''
    #     DROP TABLE Kursy_wszystkie;
    #     '''
    #
    # c.execute(sql)
    #
    # conn.commit()
    # conn.close()

    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    #
    # edytuj_kurs(c, 'kursu_prise', 799, 17)
    # edytuj_kurs(c, 'kursu_kod', '2025/ŻJw9', 11)
    #
    # conn.commit()
    # conn.close()

    #############################################
    ###########  Zaczynają się selecty:

    ...

    ...
    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    #
    # sql = '''
    #     SELECT * FROM Klientela join zapisy_na_Kursy ON uczestniko_lp=uczest_lp;
    #     '''
    #
    # c.execute(sql)
    # kolec = c.fetchall()
    # for el in kolec:
    #     print(el)
    # conn.commit()
    # conn.close()

    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    #
    # sql = '''
    #         SELECT * FROM zapisy_na_Kursy join Klientela ON uczestniko_lp=uczest_lp WHERE krs_lp = 8;
    #         '''
    #
    # c.execute(sql)
    # kolec1 = c.fetchall()
    # sql = '''
    #             SELECT * FROM zapisy_na_Kursy join Uczest_under18 ON uczestU18_lp=uczU18_lp WHERE krs_lp = 8;
    #             '''
    #
    # c.execute(sql)
    # kolec2 = c.fetchall()
    # for el in kolec1:
    #     print(el)
    # for el in kolec2:
    #     print(el)
    # conn.commit()
    # conn.close()
    # print()
    #
    # print('%%%%%%%%%%%%%%%%%%%%%')
    #
    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    #
    # sql = '''
    #         SELECT * FROM Klientela join zapisy_na_Kursy ON uczestniko_lp=uczest_lp and krs_lp like "5";
    #         '''
    #
    # c.execute(sql)
    # jeryc = c.fetchall()
    # for el in jeryc:
    #     print(el)
    # conn.commit()
    # conn.close()
    #
    # print('%%%%%%%%%%%%%%%%%%%%%')
    #
    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    #
    # sql = '''
    #     SELECT * FROM Klientela join zapisy_na_Kursy ON uczestniko_lp=uczest_lp and uczestniko_lp like "10";
    #     '''
    #
    # c.execute(sql)
    # jerko = c.fetchall()
    # for el in jerko:
    #     print(el)
    # conn.commit()
    # conn.close()
    #
    # print('%%%%%%%%%%%%%%%%%%%%%')
    #
    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    #
    # sql = '''
    #     SELECT * FROM Klientela join zapisy_na_Kursy ON uczestniko_lp=uczest_lp and uczestniko_lp like "10";
    #     '''
    #
    # c.execute(sql)
    # jerko1 = c.fetchall()
    # for el in jerko1:
    #     print(el)
    # conn.commit()
    # conn.close()
    #
    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    #
    # sql = '''
    #         SELECT * FROM zapisy_na_Kursy join Kursy_wszystkie ON krs_lp=kursu_lp and uczest_lp like "10";
    #         '''
    #
    # c.execute(sql)
    # jerko2 = c.fetchall()
    # for el in jerko2:
    #     print(el)
    # conn.commit()
    # conn.close()
    #
    # for i,j in enumerate(jerko1):
    #     lacznik = ''
    #     for el in jerko2[i][5:]:
    #         if lacznik:
    #             lacznik += ', '+str(el)
    #         else:
    #             lacznik += str(el)
    #     print(f'{j[1]} {j[2]} ({j[0]}, {j[3]}, {j[4]}) w dniu {jerko2[i][3]} zapisało się na kurs o nr porz. {jerko2[i][4]}: {lacznik}.')
    #
    # ######################################################3
    # ####
    # print()
    # print('""""""&&&&&&&&&&&&&""""""""""""""""&&&&&&&&&&&&&&&""""""""""""')
    # print()

    ...
    # ###########            A najlepiej tak:
    #
    # nameToFind = []
    # surnameToFind = []
    # emailToFind = []
    # phoneToFind = []
    #
    # list_of_wanted = find_person_lp_by_data('+48224434801')
    # for el in list_of_wanted:
    #     print(el)

    # user_lpToFind = [17]
    # this_assingment = looking_for_person(user_lpToFind)


    ##################################################################################################################
    ##################################################################################################################

    #####                    Wyświetlenie uczestników kursów o wskazanych numerach kursów

    # list_kursu_lp_to_show = [8,13]
    # conn = sqlite3.connect(bazaD)
    # c = conn.cursor()
    # wybrane_kursy = []
    # for twer in list_kursu_lp_to_show:
    #     print()
    #     ten = display_some_training(c, twer)
    #     wybrane_kursy.append(ten)
    #     print('"""""""""""""""""""""""""""""""""""""""""""""""""""')
    #
    # # conn.commit()
    # conn.close()
    # print()
    # for el in wybrane_kursy:
    #     print(el)
    
    
    ##################################################################################################################
    ##################################################################################################################
