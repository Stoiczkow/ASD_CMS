from django.db import models
from django.contrib.auth.models import User
# Create your models here.
CAUSES = (
    (1, "Cause"),
)

class Machine(models.Model):
    name = models.CharField(max_length=512, verbose_name='Nazwa maszyny')
    setting = models.IntegerField(verbose_name='Nastawa maszyny')

    class Meta:
        verbose_name = 'Maszyna'
        verbose_name_plural = "Maszyny"

    def __str__(self):
        return self.name

    @property
    def orders(self):
        return Order.objects.filter(machine=self, is_taken=False)


class Order(models.Model):
    order_id = models.IntegerField(unique=True, verbose_name="Numer zlecenia")
    start_date = models.DateTimeField(null=True, blank=True, verbose_name="Start zlecenia")
    stop_date = models.DateTimeField(null=True, blank=True, verbose_name="Koniec zlecenia")
    realization = models.FloatField(null=True, blank=True, verbose_name="Wykonano")
    planned = models.FloatField(verbose_name="Planowane wykonanie")
    is_taken = models.BooleanField(default=False, verbose_name="Zlecenie zajęte")
    is_finished = models.BooleanField(default=False, verbose_name="Zlecenie zakończone")
    waste = models.FloatField(null=True, blank=True, verbose_name="Ilość odpadów")
    machine = models.ForeignKey(Machine, on_delete=True, verbose_name="Maszyna")
    user = models.ForeignKey(User, on_delete=True, null=True, blank=True, verbose_name="Osoba odpowiedzialna")

    class Meta:
        verbose_name = 'Zlecenie'
        verbose_name_plural = "Zlecenia"

    def __str__(self):
        return "Zlecenie nr {}".format(self.order_id)


class Interruption(models.Model):
    start_date = models.DateTimeField(verbose_name="Początek przestoju")
    stop_date = models.DateTimeField(verbose_name="Koniec przestoju")
    cause = models.IntegerField(choices=CAUSES, verbose_name="Przyczyna przestoju")
    order = models.ForeignKey(Order, on_delete=True, verbose_name="Zlecenie")

    class Meta:
        verbose_name = 'Przestój'
        verbose_name_plural = "Przestoje"
