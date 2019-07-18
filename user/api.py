import os
import time

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render

from common import errors, cache_keys
from common.utils import is_phone_num
from lib.http import render_json
from swiperTest import settings
from user import logics
from user.forms import ProfieldForm
from user.models import User



#yans
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
        if logics.send_verify_code(phone_num):
            return render_json()
        else:
            return render_json(code=errors.SMS_SEND_ERR)
    else:
        return render_json(code=errors.PHONE_NUM_ERR)


def login(request):
    '''
    通过验证码登录或注册接口，如果手机号已存在，则登录，否则注册

    1、检测验证码是否正确
    2、注册或登录
    :param request:
    :return:
    '''

    #把手机号和验证码传进来， 给默认值为了去空格，避免空值
    phone_num = request.POST.get('phone_num', '')
    code = request.POST.get('code', '')

    phone_num = phone_num.strip()
    code = code.strip()

    #比较验证码
    cached_code = cache.get(cache_keys.VERIFY_CODE_CACHE_PREFIX.format(phone_num))

    if cached_code != code:
        return render_json(code=errors.VERIFY_CODE_ERR)

    # try:
    #     #检测用户
    #     user = User.objects.get(pk=1)
    # except User.DoesNotExist:
    #     #不对就注册
    #      user = User.objects.create()

    #get_or_create会返回两个值，存在记录就get，否则create
    user, created = User.objects.get_or_create(phonenum=phone_num)

    #设置登录状态
    request.session['uid'] = user.id

    # token 认证方式
    # 为当前登录用户生成一个 token，并且存储到 缓存中，key为：token:user.id，Value为：token
    # token = user.get_or_create_token()
    # data = {'token': token}
    # return render_json(data=data)

    return render_json(data=user.to_dict())

# 获取你的兴趣
def get_profile(request):

    user = request.user
    print(user.profile.to_dict())

    return render_json(data=user.profile.to_dict(exclude=['auto_play']))

#修改你的兴趣
def set_profile(request):

    user = request.user

    #通过psot参数实例化
    form = ProfieldForm(data=request.POST, instance=user.profile)
    if form.is_valid():
        form.save()
        return render_json()

    else:
        return render_json(data=form.errors)


#上传头像
def upload_avatar(request):
    '''
    这里面有三个方法：1、简单文件上传保存到本地2、保存到本地和七牛云3、异步保存
    :param request:
    :return:
    '''
    user = request.user
    avatar = request.FILES.get('avatar')

    #给头像取名字加时间戳
    file_name = 'avatar-{}'.format(int(time.time()))

    # 1、先将文件上传到本地服务器
    #
    # file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    #
    # with open(file_path, 'wb+') as destination:
    #     for chunk in avatar.chunks():
    #         destination.write(chunk)
    # return render_json()

    # file_path = logics.upload_avatar(file_name, avatar)
    #
    # # 2、将本地文件上传到七牛云
    # ret = logics.upload_qiniuyun(file_name, file_path)
    #
    # if ret:
    #     return render_json()
    # else:
    #     return render_json(code=errors.AVATAR_UPLOAD_ERR)

    logics.async_upload_avatar.delay(user, avatar)

    return render_json()