# 订单信息管理试图文件
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from datetime import datetime
from myadmin.models import Orders, OrderDetail, Payment, User, Member


def index(request, pIndex=1):
    # 浏览订单信息
    umod = Orders.objects
    sid = request.session['shopinfo']['id']  # 获取当前店铺id号
    ulist = umod.filter(status__lt=9)
    mywhere = []

    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append("status=" + status)

    # 执行分页
    pindex = int(pIndex)
    page = Paginator(ulist, 10)
    maxpage = page.num_pages
    if pindex < 1:
        pindex = 1
    elif pindex > maxpage:
        pindex = maxpage
    ulist1 = page.page(pindex)
    plist = page.page_range

    for vo in ulist1:
        if vo.user_id == 0:
            vo.nickname = '无'
        else:
            user = User.objects.only("nickname").get(id=vo.user_id)
            vo.nickname = user.nickname

        if vo.member_id == 0:
            vo.membername = '大堂点餐'
        else:
            member = Member.objects.only('mobile').get(id=vo.member_id)
            vo.membername = member.nickname

    context = {"orderslist": ulist1, 'pagelist': plist, 'pIndex': pindex, 'mywhere': mywhere, 'maxpage': maxpage}
    return render(request, 'web/list.html', context)


def insert(request, pIndex=1):
    # 执行订单添加
    try:
        # 执行订单数据的添加
        od = Orders()
        od.shop_id = request.session['shopinfo']['id']
        od.member_id = 0
        od.user_id = request.session['webuser']['id']
        od.money = request.session['total_money']
        od.status = 1  # 订单状态：1.进行中/2.无效/3.已完成
        od.payment_status = 2  # 支付状态：1.未支付/2.已支付/3.已退款
        od.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.save()

        # 执行支付信息添加
        op = Payment()
        op.order_id = od.id  # 订单id号
        od.member_id = 0
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

        return HttpResponse("Y")
    except Exception as err:
        print(err)
        return HttpResponse("N")


def detail(request):
    # 加载订单详情
    oid = request.GET.get('oid', 0)
    dlist = OrderDetail.objects.filter(order_id=oid)
    context = {'detaillist': dlist}
    return render(request, 'web/detail.html', context)


def status(request):
    # 修改订单状态
    try:
        oid = request.GET.get('oid', 0)
        ob = Orders.objects.get(id=oid)
        ob.status = request.GET['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        return HttpResponse('Y')
    except:
        return HttpResponse('N')
