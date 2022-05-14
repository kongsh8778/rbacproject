# @Time : 2022/5/8 16:43 
# @Author : kongsh
# @File : role.py
from django.shortcuts import HttpResponse, render, redirect
from django.shortcuts import reverse
from rbac import models
from rbac.forms.permissions import RoleModelForm


def role_list(request):
    """角色列表"""
    query_set = models.Role.objects.all()
    return render(request, 'rbac/role_list.html', {'query_set': query_set})


def role_add(request):
    """添加角色"""
    if request.method == "GET":
        form = RoleModelForm()
        return render(request, 'rbac/role_add_edit.html', {'form': form})
    else:
        form = RoleModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:role_list'))
    return render(request, 'rbac/role_add_edit.html', {'form': form})


def role_edit(request, uid):
    """编辑角色"""
    obj = models.Role.objects.filter(id=uid).first()
    if not obj:
        return HttpResponse("角色不存在")
    if request.method == "GET":
        form = RoleModelForm(instance=obj)
        return render(request, 'rbac/role_add_edit.html', {'form': form})
    else:
        form = RoleModelForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:role_list'))

    return render(request, 'rbac/role_add_edit.html', {'form': form})


def role_del(request, uid):
    """删除角色"""
    obj = models.Role.objects.filter(id=uid).first()
    if not obj:
        return HttpResponse("角色不存在")
    else:
        obj.delete()
        return redirect(reverse('rbac:role_list'))
