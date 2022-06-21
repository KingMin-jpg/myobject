# 会员信息管理的视图文件
from django.db.models import Q
from django.shortcuts import render
from myadmin.models import Member
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import datetime
import random


def index(request, pIndex=1):
    # 浏览信息
    umod = Member.objects
    ulist = umod.filter(status__lt=9)
    mywhere = []

    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append("status=" + status)

    # 执行分页
    pindex = int(pIndex)
    page = Paginator(ulist, 5)
    maxpage = page.num_pages
    if pindex < 1:
        pindex = 1
    elif pindex > maxpage:
        pindex = maxpage
    ulist1 = page.page(pindex)
    plist = page.page_range
    context = {"memberlist": ulist1, 'pagelist': plist, 'pIndex': pindex, 'mywhere': mywhere}
    return render(request, 'myadmin/member/index.html', context)


def delete(request, mid=0):
    # 执行删除信息操作
    try:
        ob = Member.objects.get(id=mid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': '删除成功！'}
    except Exception as err:
        print(err)
        context = {'info': '删除失败！'}
    return JsonResponse(context)
