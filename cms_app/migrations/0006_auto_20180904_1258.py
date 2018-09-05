# Generated by Django 2.0.5 on 2018-09-04 10:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms_app', '0005_auto_20180904_1242'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='interruption',
            options={'verbose_name': 'Przestój', 'verbose_name_plural': 'Przestoje'},
        ),
        migrations.AlterModelOptions(
            name='machine',
            options={'verbose_name': 'Maszyna', 'verbose_name_plural': 'Maszyny'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Zlecenie', 'verbose_name_plural': 'Zlecenia'},
        ),
        migrations.AlterField(
            model_name='interruption',
            name='cause',
            field=models.IntegerField(choices=[(1, 'Cause')], verbose_name='Przyczyna przestoju'),
        ),
        migrations.AlterField(
            model_name='interruption',
            name='order',
            field=models.ForeignKey(on_delete=True, to='cms_app.Order', verbose_name='Zlecenie'),
        ),
        migrations.AlterField(
            model_name='interruption',
            name='start_date',
            field=models.DateTimeField(verbose_name='Początek przestoju'),
        ),
        migrations.AlterField(
            model_name='interruption',
            name='stop_date',
            field=models.DateTimeField(verbose_name='Koniec przestoju'),
        ),
        migrations.AlterField(
            model_name='machine',
            name='name',
            field=models.CharField(max_length=512, verbose_name='Nazwa maszyny'),
        ),
        migrations.AlterField(
            model_name='machine',
            name='setting',
            field=models.IntegerField(verbose_name='Nastawa maszyny'),
        ),
        migrations.AlterField(
            model_name='order',
            name='is_finished',
            field=models.BooleanField(default=False, verbose_name='Zlecenie zakończone'),
        ),
        migrations.AlterField(
            model_name='order',
            name='is_taken',
            field=models.BooleanField(default=False, verbose_name='Zlecenie zajęte'),
        ),
        migrations.AlterField(
            model_name='order',
            name='machine',
            field=models.ForeignKey(on_delete=True, to='cms_app.Machine', verbose_name='Maszyna'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.IntegerField(unique=True, verbose_name='Numer zlecenia'),
        ),
        migrations.AlterField(
            model_name='order',
            name='planned',
            field=models.FloatField(verbose_name='Planowane wykonanie'),
        ),
        migrations.AlterField(
            model_name='order',
            name='realization',
            field=models.FloatField(blank=True, null=True, verbose_name='Wykonano'),
        ),
        migrations.AlterField(
            model_name='order',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Start zlecenia'),
        ),
        migrations.AlterField(
            model_name='order',
            name='stop_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Koniec zlecenia'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=True, to=settings.AUTH_USER_MODEL, verbose_name='Osoba odpowiedzialna'),
        ),
        migrations.AlterField(
            model_name='order',
            name='waste',
            field=models.FloatField(blank=True, null=True, verbose_name='Ilość odpadów'),
        ),
    ]