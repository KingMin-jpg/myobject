# 自定义中间件类
from django.shortcuts import redirect
from django.urls import reverse

import re


class ShopMiddleWare(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 获取当前请求路径
        path = request.path
        # print("mycall..."+path)

        # 后台请求路由判断
        # 定义网站后台不用登录也可访问的路由url
        myadminurllist = ['/myadmin/login', '/myadmin/dologin', '/myadmin/logout', '/myadmin/verifycode']
        # 判断当前请求是否是访问网站后台,并且path不在urllist中
        if re.match(r"^/myadmin", path) and (path not in myadminurllist):
            # 判断当前用户是否没有登录
            if "adminuser" not in request.session:
                # 执行登录界面跳转
                return redirect(reverse('myadmin_login'))

        weburllist = ['/web/login', '/web/dologin', '/web/logout', '/web/verify']
        # 判断当前请求是否是访问点餐前台,并且path不在weburllist中
        if re.match(r"^/web", path) and (path not in weburllist):
            # 判断当前用户是否没有登录
            if "webuser" not in request.session:
                # 执行登录界面跳转
                return redirect(reverse('web_login'))

        mobileurllist = ['/mobile/register', '/mobile/doRegister']
        # 判断当前请求是否是访问会员移动端,并且path不在mobileurllist中
        if re.match(r"^/mobile", path) and (path not in mobileurllist):
            # 判断当前用户是否没有登录
            if "mobileuser" not in request.session:
                # 执行登录界面跳转
                return redirect(reverse('mobile_register'))

        # 请求继续执行下去
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response
