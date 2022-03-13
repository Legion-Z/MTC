from os.path import expanduser, isfile, join
from genericpath import exists
from datetime import date
from os import listdir
import gzip



log_dir = expanduser("~") + '/log'
today = date.today()
current_month = today.strftime('%Y%m')
current_day = today.strftime('%Y%m%d')

if exists(log_dir):
  total_success = 0
  file_names = [f for f in listdir(log_dir) if isfile(join(log_dir, f))]
  cur_month_files = list(filter(lambda fn: str(fn).find(current_month) > 0, file_names))
  cur_day_files = list(filter(lambda fn: str(fn).find(current_day) > 0, cur_month_files))

  for f_name in cur_month_files:
    with gzip.open(join(log_dir, f_name), 'rt') as in_file:
      with open(join(log_dir, 'Error.log'), 'w', encoding='utf-8') as out_file:
        for line in in_file:
          if line.find('Error') > -1:
            out_file.write(line)
  
  for f_name in cur_day_files:
    with gzip.open(join(log_dir, f_name), 'rt') as in_file:
      for line in in_file:
        if line.find('Success') > -1:
          total_success += 1

  print('total count of success messages is', total_success)
  
else:
  print(log_dir,'does not exists.')