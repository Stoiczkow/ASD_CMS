import datetime
import glob
import os
import re


today = str(datetime.datetime.now().date()).replace('-', '')

os.chdir("C:/Users/v-pawel.wyzykowski/Desktop")
file_name = ''

for i in glob.glob("*.txt"):
    if i.startswith(today):
        file_name = i

with open(file_name) as file:
    print(file.readlines()[1])
