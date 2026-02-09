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
