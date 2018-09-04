from django.db import models
from django.contrib.auth.models import User
# Create your models here.
CAUSES = (
    (1, "Cause"),
)

class Machine(models.Model):
    name = models.CharField(max_length=512)
    setting = models.IntegerField()


class Order(models.Model):
    order_id = models.IntegerField(unique=True)
    start_date = models.DateTimeField()
    stop_date = models.DateTimeField()
    realization = models.FloatField()
    planned = models.FloatField()
    is_taken = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    waste = models.FloatField()
    machine = models.ForeignKey(Machine, on_delete=True)
    user = models.ForeignKey(User, on_delete=True, null=True)


class Interruption(models.Model):
    start_date = models.DateTimeField()
    stop_date = models.DateTimeField()
    cause = models.IntegerField(choices=CAUSES)
    order = models.ForeignKey(Order, on_delete=True)
