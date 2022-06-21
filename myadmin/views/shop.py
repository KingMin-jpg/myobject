# 店铺信息管理的视图文件
from django.shortcuts import render
from myadmin.models import Shopp
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from datetime import datetime
import time


def index(request, pIndex=1):
    # 浏览信息
    smod = Shopp.objects
    slist = smod.filter(status__lt=9)
    mywhere = []

    # 获取并判断搜索条件
    kw = request.GET.get('keyword', None)
    if kw:
        slist = slist.filter(name__contains=kw)
        mywhere.append("keyword=" + kw)

    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        slist = slist.filter(status=status)
        mywhere.append("status=" + status)

    slist = slist.order_by('id')

    # 执行分页
    pindex = int(pIndex)
    page = Paginator(slist, 5)
    maxpage = page.num_pages
    if pindex < 1:
        pindex = 1
    elif pindex > maxpage:
        pindex = maxpage
    slist1 = page.page(pindex)
    plist = page.page_range
    context = {"shoplist": slist1, 'pagelist': plist, 'pIndex': pindex, 'mywhere': mywhere}
    return render(request, 'myadmin/shop/index.html', context)


def add(request):
    # 加载信息添加表单
    return render(request, 'myadmin/shop/add.html')


def insert(request):
    # 执行信息添加操作
    try:
        # 店铺封面图片的上传处理
        myfile = request.FILES.get("cover_pic", None)
        if not myfile:
            return HttpResponse("没有店铺封面上传文件信息")
        cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/" + cover_pic, "wb+")
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        # 店铺logo图片的上传处理
        myfile = request.FILES.get("banner_pic", None)
        if not myfile:
            return HttpResponse("没有店铺logo上传文件信息")
        banner_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/" + banner_pic, "wb+")
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        ob = Shopp()
        ob.name = request.POST.get('name')
        ob.nickname = request.POST.get('nickname')
        ob.phone = request.POST.get('phone')
        ob.address = request.POST.get('address')
        ob.cover_pic = cover_pic
        ob.banner_pic = banner_pic
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': '添加成功！'}
    except Exception as err:
        print(err)
        context = {'info': '添加失败！'}
    return render(request, 'myadmin/info.html', context)


def delete(request, sid=0):
    # 执行删除信息操作
    try:
        ob = Shopp.objects.get(id=sid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': '删除成功！'}
    except Exception as err:
        print(err)
        context = {'info': '删除失败！'}
    return JsonResponse(context)


def edit(request, sid=0):
    # 加载信息编辑表单
    try:
        ob = Shopp.objects.get(id=sid)
        context = {'shop': ob}
        return render(request, 'myadmin/shop/edit.html', context)
    except:
        context = {'info': '没有找到要修改的店铺信息！'}
        return render(request, 'myadmin/info.html', context)


def update(request, sid):
    # 执行信息更新操作
    try:
        ob = Shopp.objects.get(id=sid)
        ob.name = request.POST.get('name')
        ob.nickname = request.POST.get('nickname')
        ob.phone = request.POST.get('phone')
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': '修改成功！'}
    except:
        context = {'info': '修改失败！'}
    return render(request, 'myadmin/info.html', context)
