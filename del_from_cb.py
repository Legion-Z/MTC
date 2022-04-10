import requests as rq
from time import sleep
import sys
import os
from os import path
from loguru import logger




def del_single_msisdn(msisdn: str) -> bool: 
    resp = rq.request('DELETE',f'http://u00-freecom-app01:8080/service-free-com-customerapi/restapi/customer/MSISDN/{msisdn}/')

    if resp.status_code == 200:
        logger.info(f'{msisdn} deleted from CashBack')
    else:
        logger.error(f'something goes wrong for {msisdn}', resp.json)


def validate_msisdn(msisdn: str):
    clean_msisdn = "".join(c for c in msisdn.strip().strip(',') if c.isdecimal())
    if len(clean_msisdn) != 11:
        logger.error("Incorrect MSISDN: " + msisdn)
        return False
    return clean_msisdn

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Script usage: python del_from_cb.py "input_file_name"')
    else:
        log_file_name = path.join(os.path.dirname(os.path.abspath(__file__)), 'delete_from_cb.log')
        logger.add(log_file_name, format="{time} {level} {name} {line} {message}", level="DEBUG", rotation="1 MB", compression="zip")

        input_f_name =  path.join(path.dirname(__file__), sys.argv[1])
        print(f'Started processing {sys.argv[1]}')
        
        in_file = open(input_f_name, 'r', encoding='utf-8')
        lines = in_file.readlines()

        for line in lines:
            valid_msisdn = validate_msisdn(line)
            if valid_msisdn:
                del_single_msisdn(valid_msisdn)
            sleep(0.5)

        print(f'{len(lines)} MSISDNs deleted from CashBack successfully.')
