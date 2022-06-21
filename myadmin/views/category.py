# 菜品类别信息管理的视图文件
from django.shortcuts import render
from myadmin.models import Category, Shopp
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import datetime
import random


def index(request, pIndex=1):
    # 浏览信息
    cmod = Category.objects
    slist = Shopp.objects
    clist = cmod.filter(status__lt=9)
    mywhere = []

    # 获取并判断搜索条件
    kw = request.GET.get('keyword', None)
    if kw:
        clist = clist.filter(name__contains=kw)
        mywhere.append("keyword=" + kw)

    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        clist = clist.filter(status=status)
        mywhere.append("status=" + status)

    for c in clist:
        smod = slist.get(id=c.shop_id)
        c.shopname = smod.name

    # 执行分页
    pindex = int(pIndex)
    page = Paginator(clist, 10)
    maxpage = page.num_pages
    if pindex < 1:
        pindex = 1
    elif pindex > maxpage:
        pindex = maxpage
    clist1 = page.page(pindex)
    plist = page.page_range
    context = {"categorylist": clist1, 'pagelist': plist, 'pIndex': pindex, 'mywhere': mywhere}
    return render(request, 'myadmin/category/index.html', context)


def add(request):
    slist = Shopp.objects.values('id', 'name')
    context = {'shoplist': slist}
    # 加载信息添加表单
    return render(request, 'myadmin/category/add.html', context)


def insert(request):
    # 执行信息添加操作
    try:
        ob = Category()
        ob.shop_id = request.POST.get('shop_id')
        ob.name = request.POST.get('name')
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': '添加成功！'}
    except Exception as err:
        print(err)
        context = {'info': '添加失败！'}
    return render(request, 'myadmin/info.html', context)


def delete(request, cid=0):
    # 执行删除信息操作
    try:
        ob = Category.objects.get(id=cid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': '删除成功！'}
    except Exception as err:
        print(err)
        context = {'info': '删除失败！'}
    return JsonResponse(context)


def edit(request, cid=0):
    # 加载信息编辑表单
    try:
        ob = Category.objects.get(id=cid)
        slist = Shopp.objects.values('id', 'name')
        context = {'category': ob, 'shoplist': slist}
        return render(request, 'myadmin/category/edit.html', context)
    except:
        context = {'info': '没有找到要修改的菜品分类信息！'}
        return render(request, 'myadmin/info.html', context)


def update(request, cid):
    # 执行信息更新操作
    try:
        ob = Category.objects.get(id=cid)
        ob.shop_id = request.POST['shop_id']
        ob.name = request.POST['name']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': '修改成功！'}
    except:
        context = {'info': '修改失败！'}
    return render(request, 'myadmin/info.html', context)


def loadCategory(request, sid):
    clist = Category.objects.filter(status__lt=9, shop_id=sid).values("id", "name")
    # 返回QuerySet对象，使用list强转成对应的菜品分类列表信息
    return JsonResponse({'data': list(clist)})
