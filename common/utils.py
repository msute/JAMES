import random
import re

PHONE_PARRERN = re.compile(r'^1[3-9]\d{9}$')


#验证手机格式
def is_phone_num(phone_num):
    if PHONE_PARRERN.match(phone_num.strip()):
        return True
    else:
        return False


#生成验证码
def gen_random_code(length=4):
    if not isinstance(length, int):
        length = 1

    if length <= 0:
        length = 1

    code = random.randrange(10 ** (length - 1), 10 ** length)

    return str(code)