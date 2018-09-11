import kronos
import datetime
import glob
import os
import re
from django.core.exceptions import ObjectDoesNotExist
from .models import Interruption

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
        current_interruption = ''
        machine_columns = [0]
        for col in machine_columns:
            for j in range(1, len(all_lines)):
                line = all_lines[j]
                print(line[:20])
                line_without_date = line[20:]
                found = re.findall(r'([0-9]+)', line_without_date)

                if not int(found[0]):
                    if not current_interruption:
                        current_interruption = str(line[0:19])
                        current_interruption_dt = datetime.datetime.strptime(current_interruption, '%d.%m.%Y %H:%M:%S')
                    try:
                        interruption = Interruption.objects.get(start_date=current_interruption_dt)
                    except ObjectDoesNotExist:
                        interruption = Interruption.objects.create(start_date=current_interruption_dt)
                else:
                    try:
                        interruption = Interruption.objects.get(start_date=datetime.datetime.strptime(current_interruption, '%d.%m.%Y %H:%M:%S'))
                        interruption.stop_date = datetime.datetime.strptime(str(line[0:19]), '%d.%m.%Y %H:%M:%S')
                        interruption.save()
                        print(interruption.stop_date)
                        print(interruption.pk)
                    except (ObjectDoesNotExist, ValueError):
                        pass
                    current_interruption = ''

# str_d = "18.07.2018 00:20:00"
# str_s = "18.07.2018 00:09:00"
# dat_obj_1 = datetime.datetime.strptime(str_d, '%d.%m.%Y %H:%M:%S')
# dat_obj_2 = datetime.datetime.strptime(str_s, '%d.%m.%Y %H:%M:%S')
# print(dat_obj_1 - dat_obj_2)