from genericpath import exists
from os import makedirs, remove
from os.path import expanduser
from random import randint
import zipfile as zf
import gzip

log_dir = expanduser("~") + '/log'
f_name_p1 = '/smbp_2022'
f_name_p2 = '_app01.log'
files_cnt = 200
lines_cnt = 70
range_month = 4
range_day = 30
log_type = ('Success', 'Info', 'Error')

if not exists(log_dir):
  makedirs(log_dir)

for i in range(files_cnt):

  f_name_rnd_month = str(randint(1,range_month))

  if len(f_name_rnd_month) < 2:
    f_name_rnd_month = '0' + f_name_rnd_month 

  f_name_rnd_day = str(randint(1,range_day))

  if len(f_name_rnd_day) < 2:
    f_name_rnd_day = '0' + f_name_rnd_day 

  f_name = log_dir + f_name_p1 + f_name_rnd_month + f_name_rnd_day + '_' + str(randint(0,100000)) + f_name_p2
  with open(f_name, 'w', encoding='utf-8') as file:
    for i in range(lines_cnt):
      file.write('{0}/{1}/{1} {3} Log from ip:.....  service.....\n'.format(
        randint(0,100000000), f_name_rnd_month, f_name_rnd_day, log_type[randint(0,2)]
          )
        )
      
  with open(f_name, 'r', encoding='utf-8') as file_in:
    with gzip.open(f_name+'.gz', 'wt') as file_out:
      file_out.writelines(file_in)

  remove(f_name)

print('logfiles were created in', log_dir, 'successfully.')