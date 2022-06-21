# 菜品信息管理的视图文件
from django.shortcuts import render
from myadmin.models import Product, Category, Shopp
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from datetime import datetime
import time, os


def index(request, pIndex=1):
    # 浏览信息
    pmod = Product.objects
    plist = pmod.filter(status__lt=9)
    mywhere = []

    # 获取并判断搜索条件
    kw = request.GET.get('keyword', None)
    if kw:
        plist = plist.filter(name__contains=kw)
        mywhere.append("keyword=" + kw)

    # 获取、判断并封装状态status搜索条件
    cid = request.GET.get('category_id', '')
    if cid != '':
        plist = plist.filter(category_id=cid)
        mywhere.append("category_id=" + cid)

    # 获取、判断并封装类别搜索条件
    status = request.GET.get('status', '')
    if status != '':
        plist = plist.filter(status=status)
        mywhere.append("status=" + status)

    for p in plist:
        smod = Shopp.objects.get(id=p.shop_id)
        cmod = Category.objects.get(id=p.category_id)
        p.shopname = smod.name
        p.categoryname = cmod.name

    # 执行分页
    pindex = int(pIndex)
    page = Paginator(plist, 10)
    maxpage = page.num_pages
    if pindex < 1:
        pindex = 1
    elif pindex > maxpage:
        pindex = maxpage
    plist1 = page.page(pindex)
    pagelist = page.page_range
    context = {"productlist": plist1, 'pagelist': pagelist, 'pIndex': pindex, 'mywhere': mywhere}
    return render(request, 'myadmin/product/index.html', context)


def add(request):
    slist = Shopp.objects.values('id', 'name')
    context = {'shoplist': slist}
    # 加载信息添加表单
    return render(request, 'myadmin/product/add.html', context)


def insert(request):
    # 执行信息添加操作
    try:
        # 图片的上传处理
        myfile = request.FILES.get("cover_pic", None)
        if not myfile:
            return HttpResponse("没有封面上传文件信息")
        cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/product/" + cover_pic, "wb+")
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        ob = Product()
        ob.shop_id = request.POST.get('shop_id')
        ob.category_id = request.POST.get('category_id')
        ob.name = request.POST.get('name')
        ob.cover_pic = cover_pic
        ob.price = request.POST['price']
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': '添加成功！'}
    except Exception as err:
        print(err)
        context = {'info': '添加失败！'}
    return render(request, 'myadmin/info.html', context)


def delete(request, pid=0):
    # 执行删除信息操作
    try:
        ob = Product.objects.get(id=pid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': '删除成功！'}
    except Exception as err:
        print(err)
        context = {'info': '删除失败！'}
    return JsonResponse(context)


def edit(request, pid=0):
    # 加载信息编辑表单
    try:
        ob = Product.objects.get(id=pid)
        slist = Shopp.objects.values('id', 'name')
        clist = Category.objects.values('id', 'name')
        context = {'product': ob, 'shoplist': slist, 'categorylist': clist}
        return render(request, 'myadmin/product/edit.html', context)
    except Exception as err:
        print(err)
        context = {'info': '没有找到要修改的菜品信息！'}
        return render(request, 'myadmin/info.html', context)


def update(request, pid):
    # 执行信息更新操作
    global cover_pic
    try:
        # 获取原图片名
        oldpicname = request.POST['oldpicname']
        # 判断是否有文件上传
        myfile = request.FILES.get("cover_pic", None)
        if not myfile:
            cover_pic = oldpicname
        else:
            # 图片的上传处理
            cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
            destination = open("./static/uploads/product/" + cover_pic, "wb+")
            for chunk in myfile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()

        ob = Product.objects.get(id=pid)
        ob.shop_id = request.POST['shop_id']
        ob.category_id = request.POST['category_id']
        ob.name = request.POST['name']
        ob.price = request.POST['price']
        ob.cover_pic = cover_pic
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': '修改成功！'}

        if myfile:
            os.remove("./static/uploads/product/" + oldpicname)
    except:
        context = {'info': '修改失败！'}
        myfile = request.FILES.get("cover_pic", None)
        if myfile:
            os.remove("./static/uploads/product/" + cover_pic)
    return render(request, 'myadmin/info.html', context)
