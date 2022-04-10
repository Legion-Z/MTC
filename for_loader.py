import sys
from os import path, SEEK_SET
from os.path import expanduser
from openpyxl import load_workbook
from datetime import datetime
from genericpath import exists
from os import makedirs

if __name__ == '__main__':

    out_dir = path.join(expanduser("~"), 'Documents','ForLoader')
    out_file_pref = '03-'+datetime.today().strftime('%Y%m%d')
    line_per_file = 2000 
    current_line_num = 2
    last_file_name = ''
    if len(sys.argv) != 2:
        print('Script usage: python for_loader.py "input_file_name"')
    else:
        if not exists(out_dir):
            makedirs(out_dir)

        input_f_name =  path.join(path.dirname(__file__), sys.argv[1])
        print(f'Started processing {sys.argv[1]}')
        wb = load_workbook(filename = input_f_name)
        
        sheet_ranges = wb['Лист1']
        first_line = 'IDTrans;PartnerID;CodeTrans;Customer;MSISDN;Date;Amount;Status;StatusUpdateDate;R0S;R1S;R2S;R3S;R4S;R5S;R6S;R7S;R8S;R9S;R0R;R1R;R2R;R3R;R4R;R5R;R6R;R7R;R8R;R9R;R0D;R1D;R2D;R3D;R4D;R5D;R6D;R7D;R8D;R7D;R9D\n'
        i = 0
        while sheet_ranges['A'+str(current_line_num)].value:
            i += 1
            out_file_name = path.join(out_dir, out_file_pref + f"{i:06d}" + '-CB-'+'03.csv')
            with open(out_file_name, 'w', encoding='ascii') as out_f:
                j = 1
                out_f.write(str(line_per_file) + ';' + first_line)
                while j <= line_per_file and sheet_ranges['A'+str(current_line_num)].value:
                    st = ';'.join([str(j), str(sheet_ranges['B'+str(current_line_num)].value), str(sheet_ranges['C'+str(current_line_num)].value),
                                        str(sheet_ranges['D'+str(current_line_num)].value), str(sheet_ranges['E'+str(current_line_num)].value).replace('None',''),
                                        str(sheet_ranges['F'+str(current_line_num)].value), str(sheet_ranges['G'+str(current_line_num)].value),
                                        str(sheet_ranges['H'+str(current_line_num)].value), str(sheet_ranges['I'+str(current_line_num)].value),
                                        str(sheet_ranges['J'+str(current_line_num)].value), 
                                        '','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','\n']) 
                    out_f.write(st)
                    j += 1
                    current_line_num += 1
            last_file_name = out_file_name
        if (current_line_num - 2) % line_per_file:
            if len(str(line_per_file)) - 1 == len(str(current_line_num - 2)):
                last_file = open(last_file_name, 'r+', encoding='ascii')
                last_file.seek(0, SEEK_SET)
                last_file.write(str((current_line_num - 2) % line_per_file) + ';' + first_line[:-1])
                last_file.close()
            else:
                last_file = open(last_file_name, 'r', encoding='ascii')
                lines = last_file.readlines()
                lines[0] = str((current_line_num - 2) % line_per_file) + ';' + first_line
                last_file = open(last_file_name, 'w', encoding='ascii')
                last_file.writelines(lines)
                last_file.close()


        print(f'Files are generated in {out_dir} successfully!\n{current_line_num - 1} lines was processed')