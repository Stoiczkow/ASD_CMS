import kronos
import datetime
import glob
import os
import re
import requests
from django.core.exceptions import ObjectDoesNotExist
from .models import Interruption, Machine, Realization, DBName


@kronos.register('* * * * *')
def process_black_box():
    today = str(datetime.datetime.now().date()).replace('-', '')
    os.chdir("C:/Users/v-pawel.wyzykowski/Desktop")
    file_name = ''
    db_name = DBName.objects.get(pk=1).name
    for i in glob.glob("*.txt"):
        if i.startswith(today):
            file_name = i

    with open(file_name) as file:
        all_lines = file.readlines()

        machines = Machine.objects.all()
        for col in range(0, len(machines)):
            current_interruption = ''
            for j in range(1, len(all_lines)):
                line = all_lines[j]
                line_without_date = line[20:]
                found = re.findall(r'([0-9]+)', line_without_date)
                if not int(found[col]):
                    if not current_interruption:
                        current_interruption = str(line[0:19])
                        current_interruption_dt = datetime.datetime.strptime(
                            current_interruption, '%d.%m.%Y %H:%M:%S')
                    try:
                        interruption = Interruption.objects.using(db_name).get(
                            start_date=current_interruption_dt,
                            machine=machines[col])
                    except ObjectDoesNotExist:
                        interruption = Interruption.objects.using(db_name).create(
                            start_date=current_interruption_dt,
                            machine=machines[col])
                else:
                    try:
                        interruption = Interruption.objects.using(db_name).get(
                            start_date=datetime.datetime.strptime(
                                current_interruption, '%d.%m.%Y %H:%M:%S'),
                            machine=machines[col])
                        interruption.stop_date = datetime.datetime.strptime(
                            str(line[0:19]), '%d.%m.%Y %H:%M:%S')
                        interruption.save(using=db_name)
                    except (ObjectDoesNotExist, ValueError):
                        pass

                    current_interruption = ''


@kronos.register('* * * * *')
def fill_interruptions():
    db_name = DBName.objects.get(pk=1).name
    interruptions = Interruption.objects.using(db_name).filter(realization=None)
    for interruption in interruptions:
        if interruption.stop_date:
            try:
                realization = Realization.objects.using(db_name).get(
                    order__machine=interruption.machine,
                    start_date__lte=interruption.stop_date,
                    stop_date__gte=interruption.start_date)
            except ObjectDoesNotExist:
                continue

            interruption.realization = realization
            interruption.save(using=db_name)
        else:
            try:
                realization = Realization.objects.using(db_name).get(
                    order__machine=interruption.machine,
                    is_active=True)
                interruption.realization = realization
                interruption.save(using=db_name)
            except ObjectDoesNotExist:
                continue
