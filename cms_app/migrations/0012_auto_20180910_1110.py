# Generated by Django 2.0.5 on 2018-09-10 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms_app', '0011_auto_20180910_1051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interruption',
            name='order',
        ),
        migrations.AddField(
            model_name='interruption',
            name='realization',
            field=models.ForeignKey(null=True, on_delete=True, to='cms_app.Realization', verbose_name='Zlecenie'),
        ),
    ]
