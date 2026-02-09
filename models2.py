# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


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
    zapisu_lp = models.AutoField(primary_key=True, blank=True, null=True)
    uczest_lp = models.ForeignKey(Klientela, models.DO_NOTHING, db_column='uczest_lp', blank=True, null=True)
    krs_lp = models.ForeignKey(KursyWszystkie, models.DO_NOTHING, db_column='krs_lp', blank=True, null=True)
    uczu18_lp = models.ForeignKey(UczestUnder18, models.DO_NOTHING, db_column='uczU18_lp', blank=True, null=True)  # Field name made lowercase.
    instruk_lp = models.ForeignKey(Instruktorostwo, models.DO_NOTHING, db_column='instruk_lp', blank=True, null=True)
    data_zapisu_nakrs = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zapisy_na_Kursy'
