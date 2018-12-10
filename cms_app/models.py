# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
ETYKIECIARKA_POSITIONS = ["Operator główny", "Pomocnik operatora"]
KARTONIARKA_POSITIONS = ["Blistrzarka", "Kartoniarka", "Blistrzarka zasilanie", "Pakowanie ręczne 1",
                         "Pakowanie ręczne 2", "Zaklejanie kartonów"]

ETYKIECIARKA_CAUSES = {"Awaria": ["Awaria"],
                       "Brak Zlecenia": ["Brak zlecenia"],
                       "Inne": ["Inne"],
                       "Przerwy": ["Przerwa", "Oczekiwanie na DUR",
                                   "Oczekiwanie na KJ",
                                   "Przerwa w pakowaniu - brak presonelu DP",
                                   "Przerwa w pakowaniu - brak materialu"],
                       "Material lub Nadruk": ["Wymiana krazka z etykietami",
                                               "Wymiana folii termotransferowej",
                                               "Zerwanie tasmy",
                                               "Jakosc nadruku"],
                       "Regulacja": ["Pozycjonowanie etykiety na wkladzie",
                                     "Blokada transportera wejsciowego"],
                       "Blokada": ["Blokada transportera wejsciowego",
                                   "Blokada kola wejsciowego",
                                   "Blokada transportera wyjsciowego",
                                   "Blokada kola wyjsciowego",
                                   "Zgubiony produkt na wyjsciu", "Foto stop"],
                       "Restart": ["Restart"]}

KARTONIARKA_CAUSES = {"Awaria": ["Awaria"],
                      "Brak Zlecenia": ["Brak zlecenia"],
                      "Inne": ["Inne"],
                      "Przerwy": ["Przerwa", "Oczekiwanie na DUR",
                                  "Oczekiwanie na KJ",
                                  "Przerwa w pakowaniu - brak presonelu DP",
                                  "Przerwa w pakowaniu - brak materialu"],
                      "Material": ["Wymiana foli PVC",
                                   "Wymiana folii aluminiowej"],
                      "Blistrzarka": ["Zablokowany przeplyw produktu",
                                      "Stacja formowania blistrow",
                                      "Podawanie wkladow",
                                      "Stacja obecnosci wkladow w blistrze",
                                      "Stacja perforacji", "Stacja wycinania",
                                      "Czujniki kontrolne - blistrzarka",
                                      "Regulacja modulu podawania blistrow",
                                      "Regulacja buforu magazynowego"],
                      "Ulotki/Kartoniki": ["Podawanie ulotek",
                                           "Skladarka ulotek",
                                           "Synchronizacja ulotki wzgledem "
                                           "kartonika",
                                           "Podawanie, formowanie kartonika",
                                           "Zamykanie kartonika",
                                           "Czytnik kodu ulotki",
                                           "Czytnik kodu kartonika",
                                           "Czujnik blistra w kartoniku",
                                           "Czujnik ulotki w kartoniku",
                                           "Jakosc nadruku",
                                           "Zablokowany przeplyw produktu",
                                           "Blokada popychacza"],
                      "Zaklejarka - Tasma": ["Zaklejarka - Tasma"],
                      "Zaklejarka - Noze": ["Zaklejarka - Noze"]}


class Machine(models.Model):
    name = models.CharField(max_length=512, verbose_name='Nazwa maszyny')
    setting = models.IntegerField(verbose_name='Nastawa maszyny')
    is_taken = models.BooleanField(default=False,
                                   verbose_name="Czy maszyna jest w tej "
                                                "chwili zajeta?")

    class Meta:
        verbose_name = 'Maszyna'
        verbose_name_plural = "Maszyny"

    def __str__(self):
        return self.name

    @property
    def orders(self):
        return Order.objects.filter(machine=self, is_finished=False)


class Order(models.Model):
    order_id = models.IntegerField(unique=True, verbose_name="Numer zlecenia")
    machine = models.ForeignKey(Machine,
                                verbose_name="Maszyna")
    start_date = models.DateTimeField(null=True, blank=True,
                                      verbose_name="Start zlecenia")
    stop_date = models.DateTimeField(null=True, blank=True,
                                     verbose_name="Koniec zlecenia")
    planned = models.FloatField(verbose_name="Planowane wykonanie")
    is_finished = models.BooleanField(default=False,
                                      verbose_name="Zlecenie zakonczone")

    class Meta:
        verbose_name = 'Zlecenie'
        verbose_name_plural = "Zlecenia"

    def __str__(self):
        return "Zlecenie nr {}".format(self.order_id)


class Realization(models.Model):
    start_date = models.DateTimeField(null=True, blank=True,
                                      verbose_name="Start realizacji")
    stop_date = models.DateTimeField(null=True, blank=True,
                                     verbose_name="Koniec realizacji")
    realization = models.FloatField(null=True, blank=True,
                                    verbose_name="Wykonano")
    waste = models.FloatField(null=True, blank=True,
                              verbose_name="Ilosc odpadow")
    is_active = models.BooleanField(default=True, blank=True,
                                    verbose_name="Czy realizacja "
                                                 "jest aktywna?")
    user = models.ForeignKey(User, null=True, blank=True,
                             verbose_name="Osoba odpowiedzialna")
    order = models.ForeignKey(Order, verbose_name="Zlecenie")
    is_cast = models.BooleanField(default=False,
                                  verbose_name="Czy realizacja została obsadzona?")

    @property
    def set_is_cast(self):
        now = datetime.datetime.now()
        try:
            if self.stop_date + datetime.timedelta(days=2) < now:
                self.is_cast = True
        except:
            pass
        
    class Meta:
        verbose_name = 'Realizacja'
        verbose_name_plural = "Realizacje"

    def __str__(self):
        return "Realizacja nr {}".format(self.pk)


class Interruption(models.Model):
    start_date = models.DateTimeField(verbose_name="Poczatek przestoju")
    stop_date = models.DateTimeField(null=True, blank=True,
                                     verbose_name="Koniec przestoju")
    cause_1 = models.CharField(max_length=256, null=True, blank=True,
                               verbose_name="Przyczyna przestoju 1")
    cause_2 = models.CharField(max_length=256, null=True, blank=True,
                               verbose_name="Przyczyna przestoju 2")
    cause_3 = models.CharField(max_length=256, null=True, blank=True,
                               verbose_name="Przyczyna przestoju 3")
    realization = models.ForeignKey(Realization, null=True,
                                    verbose_name="Realizacja")
    is_closed = models.BooleanField(default=False, blank=True,
                                    verbose_name="Czy przestoj "
                                                 "jest zamkniety?")
    was_alerted = models.BooleanField(default=False, blank=True,
                                      verbose_name="Czy przestoj "
                                                   "jest zamkniety?")
    machine = models.ForeignKey(Machine,
                                verbose_name="Maszyna")

    class Meta:
        verbose_name = 'Przestoj'
        verbose_name_plural = "Przestoje"

    #@property
    #def interruption_time(self):
    #    if self.stop_date:
    #        return abs(self.start_date - self.stop_date)
    #    else:
    #        return abs(
    #            self.start_date - datetime.datetime.now(datetime.timezone.utc))


class DBName(models.Model):
    name = models.CharField(max_length=256)


class Employee(models.Model):
    first_name = models.CharField(max_length=256, verbose_name="Imię")
    last_name = models.CharField(max_length=256, verbose_name="Nazwisko")
    is_busy = models.BooleanField(default=False, verbose_name="Czy pracownik jest zajęty?")

    class Meta:
        verbose_name = 'Pracownik'
        verbose_name_plural = "Pracownicy"

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class EmployeeRealization(models.Model):
    employee = models.ForeignKey(Employee, verbose_name="Pracownik")
    realization = models.ForeignKey(Realization, verbose_name="Realizacja")
    start_date = models.DateTimeField(verbose_name="Początek pracy")
    stop_date = models.DateTimeField(null=True, blank=True, verbose_name="Koniec pracy")
    position = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Obsada'
        verbose_name_plural = "Obsady"
