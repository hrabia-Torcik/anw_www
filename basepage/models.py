from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class DzienKursu(models.Model):
    data_dnia = models.DateField(unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Dzień_kursu"
        verbose_name_plural = "Dni_kursowe"


class Instruktor(models.Model):
    imie = models.CharField(max_length=100, verbose_name="Imię")
    imie_dopelniacz = models.CharField(max_length=100, blank=True, null=True)
    nazwisko = models.CharField(max_length=150, verbose_name="Nazwisko")
    nazwisko_dopelniacz = models.CharField(max_length=150, blank=True, null=True)
    telefon = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, blank=True, null=True)
    stopien = models.CharField(max_length=50, blank=True, null=True)


    class Meta:
        verbose_name = "Instruktoro"
        verbose_name_plural = "Instruktory"

    def __str__(self):
        return f"instr. {self.imie} {self.nazwisko}"


class Klient(models.Model):
    imie = models.CharField(max_length=100, verbose_name="Imię")
    nazwisko = models.CharField(max_length=150, verbose_name="Nazwisko")
    telefon = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)

    class Meta:
        verbose_name = "Klient"
        verbose_name_plural = "Klientela"

    def __str__(self):
        return f"kliento {self.imie} {self.nazwisko}"


class Wydarzenie(models.Model):
    kod = models.CharField(unique=True, max_length=15)
    schedule = models.CharField(max_length=50)
    data_start = models.DateField()
    data_end = models.DateField()
    price = models.DecimalField(
    max_digits=6,       # Łączna liczba cyfr (np. 99 999 999.99)
    decimal_places=2,    # Liczba cyfr po przecinku (grosze)
    validators=[
        MinValueValidator(0.01, message="Cena musi być większa od zera"),
        MaxValueValidator(9000, message="Cena nie może przekraczać 9 000 zł")
    ],
    verbose_name="Cena",
    )
    price_promo = models.DecimalField(
    max_digits=6,       # Łączna liczba cyfr (np. 99 999 999.99)
    decimal_places=2,    # Liczba cyfr po przecinku (grosze)
    validators=[
        MinValueValidator(0.01, message="Cena musi być większa od zera"),
        MaxValueValidator(9000, message="Cena nie może przekraczać 9 000 zł")
    ], blank=True, null=True,
    verbose_name="promo Cena",
    )
    name = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        verbose_name = "Wydarzenie"
        verbose_name_plural = "Wydarzenia"

    def __str__(self):
        return f"{self.name} {self.kod}"


class UczestUnder18(models.Model):
    imie = models.CharField(max_length=100, verbose_name="Imię")
    nazwisko = models.CharField(max_length=150, verbose_name="Nazwisko")
    telefon = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)


    class Meta:
        verbose_name = "Niepełnoletnie"
        verbose_name_plural = "Niepełnoletni"

    def __str__(self):
        return f"niepełoletnie {self.imie} {self.nazwisko}"


class PrzypisOpiekU18(models.Model):
    opiekuno = models.ForeignKey(Klient, on_delete=models.CASCADE, related_name='do_podopieczne')
    podopieczne = models.ForeignKey(UczestUnder18, on_delete=models.CASCADE, related_name='do_opiekuno')


    class Meta:
        verbose_name = "Przypisanie podopieczniko do opiekuno"
        verbose_name_plural = "Przypisania podopiecznikostwa do opiekunostwa"


class PrzypisanieDoDniaKursu(models.Model):
    dzien_kursowy = models.ForeignKey(DzienKursu, on_delete=models.CASCADE, related_name='przypisania')
    instruktoro = models.ForeignKey(Instruktor, on_delete=models.CASCADE, related_name='wydarzenia')
    wydarzenie = models.ForeignKey(Wydarzenie, on_delete=models.CASCADE, related_name='instruktorostwo')


    class Meta:
        verbose_name = "Przypisanie instruktora do dnia Kursu"
        verbose_name_plural = "Przypisania instruktorostwa do dni Kursu"


class ZapisNaKurs(models.Model):
    kurs = models.ForeignKey(Wydarzenie, on_delete=models.CASCADE, related_name='zapisania_kursowe')
    uczestniko = models.ForeignKey(Klient, on_delete=models.CASCADE, blank=True, null=True, related_name='zapisania_uczestniko')
    uczestniko_U18 = models.ForeignKey(UczestUnder18, on_delete=models.CASCADE, blank=True, null=True, related_name='zapisania_nieletne')  # Field name made lowercase.
    instruktoro = models.ForeignKey(Instruktor, on_delete=models.CASCADE, blank=True, null=True, related_name='zapisania_instruktoro')
    data_zapisu_nakrs = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Zapisanie na Wydarzenie")
        verbose_name_plural = "Zapisania na Wydarzenia"


class PlikImportu(models.Model):

    nazwa_pliku = models.CharField(max_length=250)
    # Pliki lecą do folderu 'uploads', a nie do 'static'!
    plik = models.FileField(upload_to='imports/%Y/%m/%d/')
    # auto_now_add=True sam wstawi właściwą datę wgrania
    data_wgrania = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Plik importu"
        verbose_name_plural = "Pliki importu"

    def __str__(self):
        return f"{self.nazwa_pliku} ({self.data_wgrania.date()})"


class DaneKursuZPliku(models.Model):
    # OneToOneField oznacza: jeden wgrany plik = jeden zestaw danych
    importowany_plik = models.OneToOneField(PlikImportu, on_delete=models.CASCADE, related_name='dane')

    # Dane wyciągnięte z Excela (przykładowo):
    nazwa_kursu = models.CharField(max_length=250)
    kod_kursu = models.CharField(max_length=50, blank=True, null=True)
    liczba_uczestnikow = models.PositiveIntegerField(default=0)
    cena_bazowa = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "Dane z pliku"
        verbose_name_plural = "Dane z plików"

class WynikAnkiety(models.Model):
    PLEC_CHOICES = (('', 'Wybierz odpowiedź...'),
                    (0, 'nie odpowiem na to pytanie'),
                    (1, 'kobieta'),
                    (2, 'mężczyzna'),
                    (3, 'inna opcja'),)

    WIEK_CHOICES = (('', 'Wybierz odpowiedź...'),
                    (0, 'nie powiem'),
                    (1, '14-18 lat'),
                    (2, '18-30 lat'),
                    (3, '30-50 lat'),
                    (4, 'niemalże dojrzałym'),)

    CZY_POLECISZ_CHOICES = (('', 'Wybierz odpowiedź...'),
                            (-2, 'będę zniechęcało. Bardzo'),
                            (-1, 'odradzałobym'),
                            (0, 'ani tak, ani nie'),
                            (1, 'tak, ale...'),
                            (2, 'Tak'),)

    STARTOWA_WIEDZA_CHOICES = (('', 'Wybierz odpowiedź...'),
                               (1, 'Total tabula rasa'), (2, 'parę razy obserwowałom, jak inni obsługują jacht'),
                               (3, 'Raz czy dwa razy coś tam porobiłom na jachcie'), (4, 'Trochę się żeglowało'),
                               (5, 'Niemałe doświadczenie, również za sterem'),)

    NABYCIE_WIEDZY_CHOICES = (('', 'Wybierz odpowiedź...'),
                              (1, 'Słabo'),
                              (2, 'Może być'),
                              (3, 'Super'),)

    PROWADZENIE_REJSU_CHOICES = (('', 'Wybierz odpowiedź...'),
                                 (1, 'Niespecjalnie'),
                                 (2, 'Popłynę, ale z duszą na ramieniu'),
                                 (3, 'Tak, spoko to ogarnę'),)

    data_wyslania = models.DateTimeField(auto_now_add=True)

    plec = models.SmallIntegerField(
        choices=PLEC_CHOICES,
        verbose_name="Czy możesz określić swoją płeć?",
        validators=[MinValueValidator(0), MaxValueValidator(3)]
    )

    wiek = models.SmallIntegerField(
        choices=WIEK_CHOICES,
        verbose_name="W jakim jesteś przedziale wiekowym?",
        validators=[MinValueValidator(0), MaxValueValidator(4)]
    )

    wybrani_instruktorzy = models.ManyToManyField(Instruktor, verbose_name="Kto prowadził Twoje zajęcia na jachcie?",)


    czy_polecisz = models.SmallIntegerField(
        choices=CZY_POLECISZ_CHOICES,
        verbose_name="Czy polecisz nas znajomej osobie?",
        validators=[MinValueValidator(-2), MaxValueValidator(2)]
    )

    startowa_wiedza = models.SmallIntegerField(
        choices=STARTOWA_WIEDZA_CHOICES,  # Te same krotki, które masz (1-5)
        verbose_name="Jaki był poziom Twoich umiejętności przed kursem?",
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    nabycie_wiedzy = models.SmallIntegerField(
        choices=NABYCIE_WIEDZY_CHOICES,
        verbose_name="Jak oceniasz przyrost swoich umiejętności?",
        validators=[MinValueValidator(1), MaxValueValidator(3)]
    )

    prowadzenie_rejsu = models.SmallIntegerField(
        choices=PROWADZENIE_REJSU_CHOICES,
        verbose_name="Czy czujesz się osobą gotową do samodzielnego poprowadzenia rejsu?",
        validators=[MinValueValidator(1), MaxValueValidator(3)]
    )


    uwagi = models.TextField(blank=True, max_length=5000, verbose_name="Dodatkowe uwagi",)


    class Meta:
        verbose_name = "Wynik ankiety"
        verbose_name_plural = "Wyniki ankiet"
        ordering = ['-data_wyslania']

class OcenaSzczegolowa(models.Model):
    ankieta = models.ForeignKey(WynikAnkiety, on_delete=models.CASCADE, related_name='oceny')
    instruktor = models.ForeignKey(Instruktor, on_delete=models.CASCADE)
    ocena_punktualnosc = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    ocena_wiedza = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    ocena_nauczanie = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    ocena_zachowanie = models.SmallIntegerField(
        validators=[MinValueValidator(-2), MaxValueValidator(2)]
    )



    class Meta:
        verbose_name = "Ocena instruktoro"
        verbose_name_plural = "Oceny instruktorostwa"

class OceniajStrone(models.Model):
    FAJNOSC_CHOICES = (('', 'Wybierz odpowiedź...'),
                       (-2, 'ale słaba!'),
                       (-1, 'ma istotne wady'),
                       (0, 'jest w porządku'),
                       (1, 'fajna'),
                       (2, 'kurde, ósmy cud świata!'),)

    CZYTELNOSC_CHOICES = (('', 'Wybierz odpowiedź...'),
                          (-2, 'nie mam pojęcia, jak poruszać się po stronie'),
                          (-1, 'w pewnych miejsca nie wiadomo gdzie kliknąć'),
                          (1, 'można zrozumieć, co robić na stronie'),
                          (2, 'bardzo łatwo wszystko znaleźć'),)

    data_wyslania = models.DateTimeField(auto_now_add=True)

    fajnosc = models.SmallIntegerField(
        choices=FAJNOSC_CHOICES,
        verbose_name="Czy strona jest przyjemna w odbiorze?",
        validators=[MinValueValidator(-2), MaxValueValidator(2)]
    )

    czytelnosc = models.SmallIntegerField(
        choices=CZYTELNOSC_CHOICES,
        verbose_name="Czy łatwo jest poruszać się po stronie?",
        validators=[MinValueValidator(-2), MaxValueValidator(2)]
    )


    co_zmienic = models.TextField(blank=True, max_length=5000, verbose_name="Napisz tutaj o ewentualnych błędach, jeśli są na stronie",)
    co_dodac = models.TextField(blank=True, max_length=5000, verbose_name="Wpisz tutaj, czego Twoim zdaniem brakuje na stronie",)
    sugestie = models.TextField(blank=True, max_length=5000, verbose_name="inne uwagi",)


    class Meta:
        verbose_name = "Wynik oceny"
        verbose_name_plural = "Wyniki ocen strony"
        ordering = ['-data_wyslania']

    def __str__(self):
        return f"Ocena z dnia {self.data_wyslania.strftime('%Y-%m-%d')}"