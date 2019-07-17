import re

PHONE_PARRERN = re.compile(r'^1[3-9]\d{9}$')


def is_phone_num(phone_num):
    if PHONE_PARRERN.match(phone_num.strip()):
        return True
    else:
        return False