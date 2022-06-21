# 员工信息管理的视图文件
from django.db.models import Q
from django.shortcuts import render
from myadmin.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import datetime
import random


def index(request, pIndex=1):
    # 浏览信息
    umod = User.objects
    ulist = umod.filter(status__lt=9)
    mywhere = []

    # 获取并判断搜索条件
    kw = request.GET.get('keyword', None)
    if kw:
        ulist = ulist.filter(Q(username__contains=kw) | Q(nickname__contains=kw))
        mywhere.append("keyword=" + kw)

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
    context = {"userlist": ulist1, 'pagelist': plist, 'pIndex': pindex, 'mywhere': mywhere}
    return render(request, 'myadmin/user/index.html', context)


def add(request):
    # 加载信息添加表单
    return render(request, 'myadmin/user/add.html')


def insert(request):
    # 执行信息添加操作
    try:
        ob = User()
        ob.username = request.POST.get('username')
        ob.nickname = request.POST.get('nickname')
        ob.address = request.POST.get('address')
        # 将当前员工的密码信息做md5加密处理
        import hashlib
        md5 = hashlib.md5()
        n = random.randint(100000, 999999)
        s = request.POST.get('password') + str(n)  # 从表单获取密码并添加干扰值
        md5.update(s.encode('utf-8'))
        ob.password_hash = md5.hexdigest()  # 获取md5的值
        ob.password_salt = n
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': '添加成功！'}
    except Exception as err:
        print(err)
        context = {'info': '添加失败！'}
    return render(request, 'myadmin/info.html', context)


def delete(request, uid=0):
    # 执行删除信息操作
    try:
        ob = User.objects.get(id=uid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': '删除成功！'}
    except Exception as err:
        print(err)
        context = {'info': '删除失败！'}
    return JsonResponse(context)


def edit(request, uid=0):
    # 加载信息编辑表单
    try:
        ob = User.objects.get(id=uid)
        context = {'user': ob}
        return render(request, 'myadmin/user/edit.html', context)
    except:
        context = {'info': '没有找到要修改的员工信息！'}
        return render(request, 'myadmin/info.html', context)


def update(request, uid):
    # 执行信息更新操作
    try:
        ob = User.objects.get(id=uid)
        ob.username = request.POST['username']
        ob.nickname = request.POST['nickname']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': '修改成功！'}
    except:
        context = {'info': '修改失败！'}
    return render(request, 'myadmin/info.html', context)
