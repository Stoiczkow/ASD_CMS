import kronos
import datetime
import glob
import os
import re
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .models import Interruption, Machine, Realization


@kronos.register('* * * * *')
def process_black_box():
    today = str(datetime.datetime.now().date()).replace('-', '')
    os.chdir("C:/Users/v-pawel.wyzykowski/Desktop")
    file_name = ''

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
                        interruption = Interruption.objects.get(
                            start_date=current_interruption_dt,
                            machine=machines[col])
                    except ObjectDoesNotExist:
                        interruption = Interruption.objects.create(
                            start_date=current_interruption_dt,
                            machine=machines[col])
                else:
                    try:
                        interruption = Interruption.objects.get(
                            start_date=datetime.datetime.strptime(
                                current_interruption, '%d.%m.%Y %H:%M:%S'),
                            machine=machines[col])
                        interruption.stop_date = datetime.datetime.strptime(
                            str(line[0:19]), '%d.%m.%Y %H:%M:%S')
                        interruption.save()
                    except (ObjectDoesNotExist, ValueError):
                        pass

                    current_interruption = ''


@kronos.register('* * * * *')
def fill_interruptions():
    interruptions = Interruption.objects.filter(realization=None)
    for interruption in interruptions:
        if interruption.stop_date:
            try:
                realization = Realization.objects.get(
                    order__machine=interruption.machine,
                    start_date__lte=interruption.stop_date,
                    stop_date__gte=interruption.start_date)
            except ObjectDoesNotExist:
                continue

            interruption.realization = realization
            interruption.save()
        else:
            try:
                realization = Realization.objects.get(
                    order__machine=interruption.machine,
                    is_active=True)
                interruption.realization = realization
                interruption.save()
            except ObjectDoesNotExist:
                continue
