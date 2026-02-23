from django.db import models
import sqlite3
import datetime


class DniKursowe(models.Model):
    dnia_lp = models.AutoField(primary_key=True)
    data_dnia = models.DateField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dni_kursowe'


class Instruktorostwo(models.Model):
    instruktoro_lp = models.AutoField(primary_key=True)
    instruktoro_name = models.CharField(blank=True, null=True)
    instruktoro_surname = models.CharField(blank=True, null=True)
    instruktoro_phone = models.IntegerField()
    instruktoro_email = models.CharField()
    instruktoro_degree = models.CharField()

    class Meta:
        managed = False
        db_table = 'Instruktorostwo'


class Klientela(models.Model):
    uczestniko_lp = models.AutoField(primary_key=True)
    uczestniko_name = models.CharField(blank=True, null=True)
    uczestniko_surname = models.CharField(blank=True, null=True)
    uczestniko_phone = models.IntegerField()
    uczestniko_email = models.CharField()

    class Meta:
        managed = False
        db_table = 'Klientela'


class KursyWszystkie(models.Model):
    kursu_lp = models.AutoField(primary_key=True)
    kursu_kod = models.CharField(unique=True, blank=True, null=True)
    kursu_schedule = models.CharField(blank=True, null=True)
    kursu_data_start = models.DateField(blank=True, null=True)
    kursu_data_end = models.DateField(blank=True, null=True)
    kursu_prise = models.IntegerField(blank=True, null=True)
    kursu_name = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Kursy_wszystkie'


class UczestUnder18(models.Model):
    uczestu18_lp = models.AutoField(db_column='uczestU18_lp', primary_key=True)  # Field name made lowercase.
    uczestu18_name = models.CharField(db_column='uczestU18_name', blank=True, null=True)  # Field name made lowercase.
    uczestu18_surname = models.CharField(db_column='uczestU18_surname', blank=True, null=True)  # Field name made lowercase.
    uczestu18_phone = models.IntegerField(db_column='uczestU18_phone', blank=True, null=True)  # Field name made lowercase.
    uczestu18_email = models.CharField(db_column='uczestU18_email', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Uczest_under18'


class PrzypisOpiekU18(models.Model):
    przypisuou18_lp = models.AutoField(db_column='przypisuOU18_lp', primary_key=True)  # Field name made lowercase.
    opiek_lp = models.ForeignKey(Klientela, models.DO_NOTHING, db_column='opiek_lp', blank=True, null=True)
    u18_lp = models.ForeignKey(UczestUnder18, models.DO_NOTHING, db_column='u18_lp', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'przypis_Opiek_U18'


class PrzypisanieDoDniaKursu(models.Model):
    przypisanie_instr_lp = models.AutoField(db_column='przypisanie_Instr_lp', primary_key=True)  # Field name made lowercase.
    dnia_kursu_lp = models.ForeignKey(DniKursowe, models.DO_NOTHING, db_column='dnia_kursu_lp', blank=True, null=True)
    inst_lp = models.ForeignKey(Instruktorostwo, models.DO_NOTHING, db_column='inst_lp', blank=True, null=True)
    od_kursu_lp = models.ForeignKey(KursyWszystkie, models.DO_NOTHING, db_column='od_kursu_lp', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'przypisanie_do_dnia_Kursu'


class ZapisyNaKursy(models.Model):
    zapisu_lp = models.AutoField(primary_key=True, blank=True, null=False)
    uczest_lp = models.ForeignKey(Klientela, models.DO_NOTHING, db_column='uczest_lp', blank=True, null=True)
    krs_lp = models.ForeignKey(KursyWszystkie, models.DO_NOTHING, db_column='krs_lp', blank=True, null=True)
    uczu18_lp = models.ForeignKey(UczestUnder18, models.DO_NOTHING, db_column='uczU18_lp', blank=True, null=True)  # Field name made lowercase.
    instruk_lp = models.ForeignKey(Instruktorostwo, models.DO_NOTHING, db_column='instruk_lp', blank=True, null=True)
    data_zapisu_nakrs = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zapisy_na_Kursy'


class File(models.Model):
    # user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    filename = models.CharField(max_length=250)
    file_upload = models.FileField(upload_to='basepage/static')
    upload_date  = models.DateField(default=datetime.datetime.now())

    def __str__(self):
        return self.user.name + 'file'

class Dataset(models.Model):
    # user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    file_uploaded = models.OneToOneField(File, on_delete=models.CASCADE)

    name_user_A = models.CharField(max_length=250)
    code_user_A = models.PositiveIntegerField(null=True)
    total_user_A = models.PositiveIntegerField(null=True)
    sd_user_A = models.PositiveIntegerField(null=True)

    name_user_B = models.CharField(max_length=250)
    code_user_B = models.PositiveIntegerField(null=True)
    total_user_B = models.PositiveIntegerField(null=True)
    sd_user_B = models.PositiveIntegerField(null=True)

class WynikAnkiety(models.Model):
    PLEC_CHOICES = (('', 'Wybierz odpowiedź...'),
                    ('0', 'nie odpowiem na to pytanie'), ('K', 'kobieta'), ('M', 'mężczyzna'),
                    ('inna', 'inna opcja'))

    WIEK_CHOICES = (('', 'Wybierz odpowiedź...'),
                    ('nie', 'nie powiem'), ('nastolatek', '14-18 lat'), ('mlody_dorosly', '18-30 lat'),
                    ('sredni_wiek', '30-50 lat'), ('pozna_doroslosc', 'niemalże dojrzałym'))

    CZY_POLECISZ_CHOICES = (('', 'Wybierz odpowiedź...'),
                            ('tak', 'Tak'), ('tak_ale', 'tak, ale...'), ('neutralnie', 'ani tak, ani nie'),
                            ('odradzam', 'odradzałobym'), ('zniechecam', 'bardzo zniechęcało'))

    STARTOWA_WIEDZA_CHOICES = (('', 'Wybierz odpowiedź...'),
                               ('1', 'Total tabula rasa'), ('2', 'parę razy obserwowałom, jak inni obsługują jacht'),
                               ('3', 'Raz czy dwa razy coś tam porobiłom na jachcie'), ('4', 'Trochę się żeglowało'),
                               ('5', 'Niemałe doświadczenie, również za sterem'))

    NABYCIE_WIEDZY_CHOICES = (('', 'Wybierz odpowiedź...'),
                              ('super', 'Super'), ('moze_byc', 'Może być'), ('slabo', 'Słabo'))

    PROWADZENIE_REJSU_CHOICES = (('', 'Wybierz odpowiedź...'),
                                 ('super', 'Tak, spoko to ogarnę'), ('moze_byc', 'Popłynę, ale z duszą na ramieniu'),
                                 ('slabo', 'Niespecjalnie'))

    data_wyslania = models.DateTimeField(auto_now_add=True)

    plec = models.CharField(
        max_length=50,
        choices=PLEC_CHOICES,
        verbose_name="Czy możesz określić swoją płeć?",
    )

    wiek = models.CharField(
        max_length=50,
        choices=WIEK_CHOICES,
        verbose_name= "W jakim jesteś przedziale wiekowym?",)

    wybrani_instruktorzy = models.ManyToManyField(Instruktorostwo, verbose_name="Kto prowadził Twoje zajęcia na jachcie?",)

    czy_polecisz = models.CharField(max_length=50,
        choices=CZY_POLECISZ_CHOICES,
        verbose_name="Czy poleciłbyś nas znajomemu?",)

    startowa_wiedza = models.CharField(max_length=50,
        choices=STARTOWA_WIEDZA_CHOICES,
        verbose_name="Jaki był poziom Twoich umiejętności przed kursem?",)



    nabycie_wiedzy = models.CharField(max_length=50,
        choices=NABYCIE_WIEDZY_CHOICES,
        verbose_name="Jak oceniasz przyrost swoich umiejętności w zakresie prowadzenia jachtu?",)


    prowadzenie_rejsu = models.CharField(max_length=50,
        choices=PROWADZENIE_REJSU_CHOICES,
        verbose_name="Czy czujesz się osobą gotową do samodzielnego poprowadzenia rejsu?",)


    uwagi = models.TextField(blank=True, max_length=5000, verbose_name="Dodatkowe uwagi",)


    class Meta:
        verbose_name = "Wynik ankiety"
        verbose_name_plural = "Wyniki ankiet"
        ordering = ['-data_wyslania']

class OcenaSzczegolowa(models.Model):
    ankieta = models.ForeignKey(WynikAnkiety, on_delete=models.CASCADE, related_name='oceny')
    instruktor = models.ForeignKey(Instruktorostwo, on_delete=models.CASCADE)
    ocena_punktualnosc = models.IntegerField()
    ocena_wiedza = models.IntegerField()
    ocena_nauczanie = models.IntegerField()
    ocena_zachowanie = models.IntegerField()

class OceniajStrone(models.Model):
    FAJNOSC_CHOICES = (('', 'Wybierz odpowiedź...'),
                    ('-2', 'ale słaba!'), ('-1', 'ma istotne wady'), ('0', 'jest w porządku'),
                    ('1', 'fajna'), ('2', 'kurde, ósmy cud świata!'))

    CZYTELNOSC_CHOICES = (('', 'Wybierz odpowiedź...'),
                          ('-2', 'nie mam pojęcia, jak poruszać się po stronie'), ('-1', 'w pewnych miejsca nie wiadomo gdzie kliknąć'),
                          ('1', 'można zrozumieć, co robić na stronie'), ('2', 'bardzo łatwo wszystko znaleźć'))

    data_wyslania = models.DateTimeField(auto_now_add=True)

    fajnosc = models.CharField(
        max_length=50,
        choices=FAJNOSC_CHOICES,
        verbose_name="Czy strona jest przyjemna w odbiorze?",
    )

    czytelnosc = models.CharField(
        max_length=50,
        choices=CZYTELNOSC_CHOICES,
        verbose_name= "Czy łatwo jest poruszać się po stronie?",)


    co_zmienic = models.TextField(blank=True, max_length=5000, verbose_name="Napisz tutaj o ewentualnych błędach, jeśli są na stronie",)
    co_dodac = models.TextField(blank=True, max_length=5000, verbose_name="Wpisz tutaj, czego Twoim zdaniem brakuje na stronie",)
    sugestie = models.TextField(blank=True, max_length=5000, verbose_name="inne uwagi",)


    class Meta:
        verbose_name = "Wynik oceny"
        verbose_name_plural = "Wyniki ocen strony"
        ordering = ['-data_wyslania']