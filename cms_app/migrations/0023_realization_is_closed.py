# Generated by Django 2.0.5 on 2018-09-14 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms_app', '0022_auto_20180914_0839'),
    ]

    operations = [
        migrations.AddField(
            model_name='realization',
            name='is_closed',
            field=models.BooleanField(default=False, verbose_name='Czy przestój jest zamknięty?'),
        ),
    ]
