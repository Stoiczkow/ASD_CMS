# Generated by Django 2.0.5 on 2018-09-11 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms_app', '0016_auto_20180911_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interruption',
            name='stop_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Koniec przestoju'),
        ),
    ]
