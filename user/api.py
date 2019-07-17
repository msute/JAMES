from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from common import eorro
from common.urils import is_phone_num


def verify_phone(request):
    '''
    1,验证手机格式
    2,生成验证码
    3,保存验证码
    4,发送验证码
    :param request:
    :return:
    '''
    phone_num = request.POST.get('phone_num')

    #判断手机格式是否正确
    if is_phone_num(phone_num):
        return JsonResponse(data= {'code': eorro.OK})
    else:
        return JsonResponse(data= {'code': eorro.PHONE_NUM_ERR})