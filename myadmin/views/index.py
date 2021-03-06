from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse
from myadmin.models import User


# 加载后台管理首页
def index(request):
    return render(request, 'myadmin/index/index.html')


# 加载会员登录表单
def login(request):
    return render(request, 'myadmin/index/login.html')


# 执行登录操作
def dologin(request):
    try:
        if request.session.get('verifycode', None) == request.POST['verify']:
            ob = User.objects.get(username=request.POST['username'])
            if ob.status == 6:
                import hashlib
                md5 = hashlib.md5()
                s = request.POST.get('password') + ob.password_salt  # 从表单获取密码并添加干扰值
                md5.update(s.encode('utf-8'))  # 获取md5的值
                if ob.password_hash == md5.hexdigest():
                    request.session['adminuser'] = ob.toDict()
                    return redirect(reverse('myadmin_index'))
                else:
                    context = {'info': '用户密码错误！'}
            else:
                context = {'info': '用户权限不足！'}
        else:
            context = {'info': '验证码错误！'}
    except Exception as err:
        print(err)
        context = {'info': '用户名不存在！'}
    return render(request, 'myadmin/index/login.html', context)


# 执行退出登录操作
def logout(request):
    del request.session['adminuser']
    return redirect(reverse('myadmin_login'))


def verifycode(request):
    # 引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = '1234567890'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象
    font = ImageFont.truetype('static/myadmin/verify/arial.ttf', 23)
    # font = ImageFont.load_default().font
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
