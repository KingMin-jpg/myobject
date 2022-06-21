from django.urls import path

from myadmin.views import index
from myadmin.views import user, shop, category, product, member

urlpatterns = [
    path('', index.index, name='myadmin_index'),  # 后台首页

    # 后台管理员登录、退出路由
    path('login', index.login, name='myadmin_login'),  # 加载登录表单
    path('dologin', index.dologin, name='myadmin_dologin'),  # 执行登录操作
    path('logout', index.logout, name='myadmin_logout'),  # 执行退出登录操作

    # 验证码
    path('verifycode', index.verifycode, name='myadmin_verifycode'),

    # 员工信息管理路由
    path('user/<int:pIndex>', user.index, name='myadmin_user_index'),  # 浏览员工信息
    path('user/add', user.add, name='myadmin_user_add'),  # 加载添加员工信息表单
    path('user/insert', user.insert, name='myadmin_user_insert'),  # 执行添加员工信息操作
    path('user/delete/<int:uid>', user.delete, name='myadmin_user_delete'),  # 删除员工信息
    path('user/edit/<int:uid>', user.edit, name='myadmin_user_edit'),  # 加载修改员工信息表单
    path('user/update/<int:uid>', user.update, name='myadmin_user_update'),  # 执行员工信息更新操作

    # 店铺信息管理路由
    path('shop/<int:pIndex>', shop.index, name='myadmin_shop_index'),  # 浏览店铺信息
    path('shop/add', shop.add, name='myadmin_shop_add'),  # 加载添加店铺信息表单
    path('shop/insert', shop.insert, name='myadmin_shop_insert'),  # 执行添加店铺信息操作
    path('shop/delete/<int:sid>', shop.delete, name='myadmin_shop_delete'),  # 删除店铺信息
    path('shop/edit/<int:sid>', shop.edit, name='myadmin_shop_edit'),  # 加载修改店铺信息表单
    path('shop/update/<int:sid>', shop.update, name='myadmin_shop_update'),  # 执行店铺信息更新操作

    # 菜单分类信息管理路由
    path('category/<int:pIndex>', category.index, name='myadmin_category_index'),  # 浏览菜单分类信息
    path('category/add', category.add, name='myadmin_category_add'),  # 加载添加菜单分类信息表单
    path('category/insert', category.insert, name='myadmin_category_insert'),  # 执行添加菜单分类信息操作
    path('category/delete/<int:cid>', category.delete, name='myadmin_category_delete'),  # 删除菜单分类信息
    path('category/edit/<int:cid>', category.edit, name='myadmin_category_edit'),  # 加载修改菜单分类信息表单
    path('category/update/<int:cid>', category.update, name='myadmin_category_update'),  # 执行菜单分类信息更新操作
    path('category/load/<int:sid>', category.loadCategory, name='myadmin_category_load'),  # 加载菜品类别信息

    # 菜单信息管理路由
    path('product/<int:pIndex>', product.index, name='myadmin_product_index'),  # 浏览菜单信息
    path('product/add', product.add, name='myadmin_product_add'),  # 加载添加菜单信息表单
    path('product/insert', product.insert, name='myadmin_product_insert'),  # 执行添加菜单信息操作
    path('product/delete/<int:pid>', product.delete, name='myadmin_product_delete'),  # 删除菜单信息
    path('product/edit/<int:pid>', product.edit, name='myadmin_product_edit'),  # 加载修改菜单信息表单
    path('product/update/<int:pid>', product.update, name='myadmin_product_update'),  # 执行菜单信息更新操作

    # 会员管理路由
    path('member/<int:pIndex>', member.index, name="myadmin_member_index"),  # 浏览会员
    path('member/delete/<int:mid>', member.delete, name="myadmin_member_delete"),  # 浏览会员
]
