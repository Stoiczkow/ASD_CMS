from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
ETYKIECIARKA_CAUSES = {"Awaria": ["Awaria"],
                       "Brak Zlecenia": ["Brak zlecenia"],
                       "Inne": ["Inne"],
                       "Przerwy": ["Przerwa", "Oczekiwanie na DUR",
                                   "Oczekiwanie na KJ",
                                   "Przerwa w pakowaniu - brak presonelu DP",
                                   "Przerwa w pakowaniu - brak materiału"],
                       "Materiał lub Nadruk": ["Wymiana krążka z etykietami",
                                               "Wymiana folii termotransferowej",
                                               "Zerwanie taśmy",
                                               "Jakość nadruku"],
                       "Regulacja": ["Pozycjonowanie etykiety na wkładzie",
                                     "Blokada transportera wejściowego"],
                       "Blokada": ["Blokada transportera wejściowego",
                                   "Blokada koła wejściowego",
                                   "Blokada transportera wyjściowego",
                                   "Blokada koła wyjściowego",
                                   "Zgubiony produkt na wyjściu", "Foto stop"],
                       "Restart": ["Restart"]}

KARTONIARKA_CAUSES = {"Awaria": ["Awaria"],
                      "Brak Zlecenia": ["Brak zlecenia"],
                      "Inne": ["Inne"],
                      "Przerwy": ["Przerwa", "Oczekiwanie na DUR",
                                  "Oczekiwanie na KJ",
                                  "Przerwa w pakowaniu - brak presonelu DP",
                                  "Przerwa w pakowaniu - brak materiału"],
                      "Materiał": ["Wymiana foli PVC",
                                   "Wymiana folii aluminiowej"],
                      "Blistrzarka": ["Zablokowany przepływ produktu",
                                      "Stacja formowania blistrów",
                                      "Podawanie wkładów",
                                      "Stacja obecności wkładów w blistrze",
                                      "Stacja perforacji", "Stacja wycinania",
                                      "Czujniki kontrolne - blistrzarka",
                                      "Regulacja modułu podawania blistrów",
                                      "Regulacja buforu magazynowego"],
                      "Ulotki/Kartoniki": ["Podawanie ulotek",
                                           "Składarka ulotek",
                                           "Synchronizacja ulotki względem "
                                           "kartonika",
                                           "Podawanie, formowanie kartonika",
                                           "Zamykanie kartonika",
                                           "cCzytnik kodu ulotki",
                                           "Czytnik kodu kartonika",
                                           "Czujnik blistra w kartoniku",
                                           "Czujnik ulotki w kartoniku",
                                           "Jakość nadruku",
                                           "Zablokowany przepływ produktu",
                                           "Blokada popychacza"],
                      "Zaklejarka - Taśma": ["Zaklejarka - Taśma"],
                      "Zaklejarka - Noże": ["Zaklejarka - Noże"]}


class Machine(models.Model):
    name = models.CharField(max_length=512, verbose_name='Nazwa maszyny')
    setting = models.IntegerField(verbose_name='Nastawa maszyny')
    is_taken = models.BooleanField(default=False,
                                   verbose_name="Czy maszyna jest w tej "
                                                "chwili zajęta?")

    class Meta:
        verbose_name = 'Maszyna'
        verbose_name_plural = "Maszyny"

    def __str__(self):
        return self.name

    @property
    def orders(self):
        return Order.objects.filter(machine=self, is_finished=False)


class Order(models.Model):
    order_id = models.IntegerField(verbose_name="Numer zlecenia")
    machine = models.ForeignKey(Machine, on_delete=True,
                                verbose_name="Maszyna")
    start_date = models.DateTimeField(null=True, blank=True,
                                      verbose_name="Start zlecenia")
    stop_date = models.DateTimeField(null=True, blank=True,
                                     verbose_name="Koniec zlecenia")
    planned = models.FloatField(verbose_name="Planowane wykonanie")
    is_finished = models.BooleanField(default=False,
                                      verbose_name="Zlecenie zakończone")

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
                              verbose_name="Ilość odpadów")
    is_active = models.BooleanField(default=True, blank=True,
                                    verbose_name="Czy realizacja "
                                                 "jest aktywna?")
    user = models.ForeignKey(User, on_delete=True, null=True, blank=True,
                             verbose_name="Osoba odpowiedzialna")
    order = models.ForeignKey(Order, on_delete=True, verbose_name="Zlecenie")

    class Meta:
        verbose_name = 'Realizacja'
        verbose_name_plural = "Realizacje"

    def __str__(self):
        return "Realizacja nr {}".format(self.pk)


class Interruption(models.Model):
    start_date = models.DateTimeField(verbose_name="Początek przestoju")
    stop_date = models.DateTimeField(null=True, blank=True,
                                     verbose_name="Koniec przestoju")
    cause_1 = models.CharField(max_length=256, null=True, blank=True,
                               verbose_name="Przyczyna przestoju 1")
    cause_2 = models.CharField(max_length=256, null=True, blank=True,
                               verbose_name="Przyczyna przestoju 2")
    cause_3 = models.CharField(max_length=256, null=True, blank=True,
                               verbose_name="Przyczyna przestoju 3")
    realization = models.ForeignKey(Realization, null=True, on_delete=True,
                                    verbose_name="Realizacja")
    is_closed = models.BooleanField(default=False, blank=True,
                                    verbose_name="Czy przestój "
                                                 "jest zamknięty?")
    was_alerted = models.BooleanField(default=False, blank=True,
                                      verbose_name="Czy przestój "
                                                   "jest zamknięty?")
    machine = models.ForeignKey(Machine, on_delete=True,
                                verbose_name="Maszyna")

    class Meta:
        verbose_name = 'Przestój'
        verbose_name_plural = "Przestoje"

    @property
    def interruption_time(self):
        if self.stop_date:
            return abs(self.start_date - self.stop_date).total_seconds()/60
        else:
            return abs(
                self.start_date - datetime.datetime.now(datetime.timezone.utc)).total_seconds()/60


class DBName(models.Model):
    name = models.CharField(max_length=256)
