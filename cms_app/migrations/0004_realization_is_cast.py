# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-10 21:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms_app', '0003_employee_employeerealization'),
    ]

    operations = [
        migrations.AddField(
            model_name='realization',
            name='is_cast',
            field=models.BooleanField(default=False, verbose_name='Czy realizacja została obsadzona?'),
        ),
    ]