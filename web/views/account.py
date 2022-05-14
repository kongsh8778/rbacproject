# @Time : 2022/5/3 15:59 
# @Author : kongsh
# @File : account.py
from django.shortcuts import render, redirect
from rbac import models
from rbac.service.init_permission import init_permission


def login(request):
    """
    登陆的视图函数
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, 'login.html')
    # 1、获取提交的用户名和密码
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')

    # 2、校验是否合法
    obj = models.UserInfo.objects.filter(name=user, password=pwd).first()
    if not obj:
        return render(request, 'login.html', {'msg': '用户名或密码错误'})
    # 校验通过后写入session
    request.session['user_info'] = {
        'id': obj.pk,
        'name': obj.name
    }
    init_permission(request, obj)
    return redirect("/customer/list/")
