# Generated by Django 2.0.5 on 2018-09-11 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms_app', '0013_auto_20180911_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interruption',
            name='stop_date',
            field=models.DateTimeField(default=None, verbose_name='Koniec przestoju'),
        ),
    ]