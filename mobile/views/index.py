from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime
# from django.views.decorators.cache import cache_page

from myadmin.models import Member, Shopp, Category, Product, Orders, Payment, OrderDetail


# @cache_page(60 * 5)
def index(request):
    # 移动端首页
    mobile_shopinfo = request.session.get('mobile_shopinfo', None)
    if mobile_shopinfo is None:
        return redirect(reverse('mobile_shop'))  # 重定向到店铺选择页
    # 获取当前店铺下的菜品类别和菜品信息
    clist = Category.objects.filter(shop_id=mobile_shopinfo['id'], status=1)
    plist = dict()
    for vo in clist:
        plist[vo.id] = Product.objects.filter(category_id=vo.id, status=1)
    context = {'categorylist': clist, 'productlist': plist.items(), 'cid': clist[0]}

    return render(request, 'mobile/index.html', context)


def register(request):
    # 会员注册/登录页面
    return render(request, 'mobile/register.html')


def doRegister(request):
    # 执行会员注册/登录操作
    # 模拟短信验证
    verifycode = '1234'  # request.session['verifycode']
    if verifycode != request.POST['code']:
        context = {'info': '验证码错误！'}
        return render(request, 'mobile/register.html', context)

    try:
        # 根据手机号码获取当前会员信息
        # member = Member.objects.get(mobile=request.POST['mobile'])
        member = get_object_or_404(Member, mobile=request.POST['mobile'])
        # print(member.mobile)
        # 检验当前会员状态
        if member.status == 1:
            request.session['mobileuser'] = member.toDict()
            return redirect(reverse('mobile_index'))
        else:
            context = {'info': '此账户信息已被禁用！'}
            return render(request, 'mobile/register.html', context)
    except Exception as err:
        # print(err)
        # 执行当前会员注册
        if len(request.POST['mobile']) != 11:
            context = {'info': '请输入正确的手机号！'}
            return render(request, 'mobile/register.html', context)
        else:
            ob = Member()
            ob.nickname = '顾客'  # 默认会员名称
            ob.avatar = 'moren.png'  # 默认头像
            ob.mobile = request.POST['mobile']
            ob.status = 1
            ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ob.save()

        if Member.objects.get(mobile=request.POST['mobile']).status == 1:
            request.session['mobileuser'] = Member.objects.get(mobile=request.POST['mobile']).toDict()
            return redirect(reverse('mobile_index'))
        else:
            context = {'info': '此账户信息已被禁用！'}
            return render(request, 'mobile/register.html', context)


def shop(request):
    # 选择店铺页面
    context = {'shoplist': Shopp.objects.filter(status=1)}
    return render(request, 'mobile/shop.html', context)


def selectShop(request):
    # 执行选择店铺
    sid = request.GET.get('sid')
    ob = Shopp.objects.get(id=sid)
    request.session['mobile_shopinfo'] = ob.toDict()
    print(request.session['mobile_shopinfo'])
    request.session['cartlist'] = {}
    return redirect(reverse('mobile_index'))


def addOrders(request):
    # 移动端下单页面
    cartlist = request.session.get('cartlist', {})
    total_money = 0  # 初始化一个总金额

    if cartlist != {}:
        for i in cartlist:
            total_money += (cartlist[i]['num'] * cartlist[i]['price'])

    request.session['total_money'] = total_money  # 把总金额放进session
    return render(request, 'mobile/addOrders.html')


def doAddOrders(request):
    # 执行订单添加
    try:
        # 执行订单数据的添加
        od = Orders()
        od.shop_id = request.session['mobile_shopinfo']['id']
        od.member_id = request.session['mobileuser']['id']
        od.user_id = 0
        od.money = request.session['total_money']
        od.status = 1  # 订单状态：1.进行中/2.无效/3.已完成
        od.payment_status = 2  # 支付状态：1.未支付/2.已支付/3.已退款
        od.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.save()

        # 执行支付信息添加
        op = Payment()
        op.order_id = od.id  # 订单id号
        od.member_id = request.session['mobileuser']['id']
        op.type = 2
        op.bank = request.GET.get("bank", 3)  # 收款渠道：1.微信/2.余额/3.现金/4.支付宝
        op.money = request.session['total_money']
        op.status = 2  # 订单状态：1.进行中/2.无效/3.已完成
        op.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.save()

        # 执行订单详情的添加
        cartlist = request.session.get("cartlist", {})
        # 遍历购物车中的菜品并添加到订单详情中
        for item in cartlist.values():
            ov = OrderDetail()
            ov.order_id = od.id  # 订单id
            ov.product_id = item['id']  # 菜品id
            ov.product_name = item['name']  # 菜品名称
            ov.price = item['price']  # 单价
            ov.quantity = item['num']  # 数量
            ov.status = item['status']  # 状态:1正常/9删除
            ov.save()

        del request.session["cartlist"]
        del request.session['total_money']
    except Exception as err:
        print(err)
    return render(request, 'mobile/orderInfo.html', {'order': od})
