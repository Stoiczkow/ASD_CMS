import kronos
import datetime
import glob
import os
import re


@kronos.register('* * * * *')
def process_black_box():
    today = str(datetime.datetime.now().date()).replace('-', '')
    os.chdir("C:/Users/v-pawel.wyzykowski/Desktop")
    file_name = ''

    for i in glob.glob("*.txt"):
        if i.startswith(today):
            file_name = i

    with open(file_name) as file:
        interruptions = {}
        all_lines = file.readlines()
        current_interruption = ''
        machine_columns = [0, 1]
        for col in machine_columns:
            key_m = 'machine {}'.format(col)
            interruptions[key_m] = {}
            for j in range(1, len(all_lines)):
                line = all_lines[j]
                line_without_date = line[20:]
                found = re.findall(r'([0-9]+)', line_without_date)

                if not int(found[0]):
                    if not current_interruption:
                        current_interruption = str(line[0:19])
                    try:
                        interruptions[key_m][current_interruption][0] += 1
                    except KeyError:
                        interruptions[key_m][current_interruption] = [1]
                else:
                    try:
                        interruptions[key_m][current_interruption].append(str(line[0:19]))
                    except KeyError:
                        pass
                    current_interruption = ''
        print(interruptions)