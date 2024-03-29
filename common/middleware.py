from django.utils.deprecation import MiddlewareMixin

from common import errors
from common.errors import LogicException, LogicError
from lib.http import render_json
from user.models import User


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):

        '''
        自定义认证中间件
        白名单  request。path
        根据 request.session['uid'] 来判断登录状态
        :param request:
        :return:
        '''

        WHITE_LIST = [
            '/api/user/verify-phone',
            '/api/user/login',
        ]

        if request.path in WHITE_LIST:
            return

        uid = request.session.get('uid')

        #拿不到登录认证就报错
        if not uid:
            return render_json(code=errors.LOGIN_REQUIRED_ERR)

        request.user = User.objects.get(pk=uid)

        #token验证登录方式
        # for k,v in request.META.items():
        #     print(k, v)

        # token = request.META.get('HTTP_X_SWIPER_AHTU_TOKEN')
        # uid = cache.get(token)
        # if not token:
        #     return render_json(code=errors.LOGIN_REQUIRED_ERR)
        # request.user = User.objects.get(pk=uid)


class LogicExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, (LogicException, LogicError)):
            return render_json(code=exception.code)