from django.core.cache import cache

from common import utils, cache_keys
from lib import sms


def send_verify_code(phone_num):
    '''
    发送验证码
    :param phone_num:接收手机号
    :return:
    '''

    #生成验证码
    code = utils.gen_random_code(6)


    #发送验证码
    ret =  sms.send_verify_code(phone_num, code)

    #发送完保存,给key的prefix配置
    if ret:
        cache.set(cache_keys.VERIFY_CODE_CACHE_PREFIX.format(phone_num), code, 60 *3)

    return ret