"""
业务相关配置
"""

# 云之讯短信平台配置
YZX_SMS_URL = 'https://open.ucpaas.com/ol/sms/sendsms'

YZX_SMS_PARAMS = {
    'sid': '22ac8d51a958dc580d8503173199845c',
    'token': '8f44a2423cba9bf316d6197e88bfd3ac',
    'appid': '14595d89fddf4bbfa633f497a673a0b8',
    'templateid': '481679',
    'param': None,
    'mobile': None
}


# 七牛云存储配置
QN_ACCESS_KEY = '6Y6DNU_T2qgRZoiqRqHa3Ozr9eswSc_ldcfPT5rA' #前两个是密钥
QN_SECRET_KEY = 'JqFuzN2WUm-zIjFJVsRuCqrWTADBGvxDIXJ1aQIU'
QN_BUCKET_NAME = 'testjames'   #上传到七牛云里面建立的空间
QN_HOST = 'http://puu0bmu79.bkt.clouddn.com'  #云存储的地址

SWIPE_LIMIT = 3     # 每日滑动上限