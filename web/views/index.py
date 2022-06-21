from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from myadmin.models import Shopp, User, Category, Product


def index(request):
    # 项目前台大堂点餐首页
    return redirect(reverse('web_index'))


def webindex(request):
    # 尝试从session中获取名字为cartlist的购物车信息，若没有返回{}
    cartlist = request.session.get('cartlist', {})
    total_money = 0  # 初始化一个总金额

    if cartlist != {}:
        for i in cartlist:
            total_money += (cartlist[i]['num'] * cartlist[i]['price'])

    request.session['total_money'] = total_money  # 把总金额放进session
    # 将session中的菜品和类别信息获取并items转换，可实现for循环遍历
    context = {'categorylist': request.session.get('categorylist', {}).items()}
    return render(request, 'web/index.html', context)


def login(request):
    slist = Shopp.objects.filter(status=1)
    context = {'shoplist': slist}
    return render(request, 'web/login.html', context)


def dologin(request):
    try:
        if request.POST.get('shop_id') == '0':
            return redirect(reverse('web_login') + '?errinfo=4')
        else:
            if request.session.get('verify', None) == request.POST['verify']:
                ob = User.objects.get(username=request.POST['username'])
                import hashlib
                md5 = hashlib.md5()
                s = request.POST.get('pass') + ob.password_salt  # 从表单获取密码并添加干扰值
                md5.update(s.encode('utf-8'))  # 获取md5的值
                if ob.password_hash == md5.hexdigest():
                    request.session['webuser'] = ob.toDict()
                    # 获取当前店铺信息
                    request.session['shopinfo'] = Shopp.objects.get(id=int(request.POST['shop_id'])).toDict()
                    # 获取当前店铺的菜品分类信息和菜品信息
                    clist = Category.objects.filter(shop_id=Shopp.objects.get(id=int(request.POST['shop_id'])).id)

                    categorylist = dict()  # 菜品类别（内含有菜品信息）
                    productlist = dict()  # 菜品信息
                    # 遍历菜品类别信息
                    for vo in clist:
                        c = {'id': vo.id, 'name': vo.name, 'pids': []}
                        plist = Product.objects.filter(category_id=vo.id, status=1)
                        # 遍历当下类别的所有菜品信息
                        for p in plist:
                            c['pids'].append(p.toDict())
                            productlist[p.id] = p.toDict()
                        categorylist[vo.id] = c

                    # 将上面信息的结果分别存在session中
                    request.session['categorylist'] = categorylist
                    request.session['productlist'] = productlist

                    return redirect(reverse('web_index'))
                else:
                    return redirect(reverse('web_login') + '?errinfo=1')
            else:
                return redirect(reverse('web_login') + '?errinfo=2')
    except Exception as err:
        print(err)
        return redirect(reverse('web_login') + '?errinfo=3')


def logout(request):
    del request.session['webuser']
    return redirect(reverse('web_login'))


def verify(request):
    # 引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
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
    request.session['verify'] = rand_str
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
    print(buf.getvalue())
    return HttpResponse(buf.getvalue(), 'image/png')
