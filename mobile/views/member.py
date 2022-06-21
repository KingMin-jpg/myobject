from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.cache import cache_page

from myadmin.models import Member, Orders, OrderDetail, Shopp


@cache_page(60 * 5)
def index(request):
    # 个人中心首页
    return render(request, 'mobile/member.html')


def orders(request):
    # 个人中心浏览订单
    # 浏览订单信息
    mod = Orders.objects
    mid = request.session['mobileuser']['id']  # 获取当前会员id号
    olist = mod.filter(member_id=mid)

    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '' and status != '0':
        olist = olist.filter(status=status)

    olist1 = olist.order_by('-id')

    orders_status = ['无', '排队中', '已撤销', '已完成']

    for vo in olist1:
        plist = OrderDetail.objects.filter(order_id=vo.id)[:4]  # 获取前面4条
        vo.plist = plist
        vo.statusinfo = orders_status[vo.status]

    context = {"orderslist": olist1}
    return render(request, 'mobile/member_orders.html', context)


def detail(request):
    # 个人中心订单详情
    pid = request.GET.get('pid', 0)
    order = Orders.objects.get(id=pid)
    plist = OrderDetail.objects.filter(order_id=order.id)
    order.plist = plist
    shop = Shopp.objects.only('name').get(id=order.shop_id)
    order.shopname = shop.name
    orders_status = ['无', '排队中', '已撤销', '已完成']
    order.statusinfo = orders_status[order.status]

    return render(request, 'mobile/member_detail.html', {'order': order})


def logout(request):
    # 执行会员退出登录
    del request.session['mobileuser']
    del request.session['mobile_shopinfo']
    return render(request, 'mobile/register.html')
