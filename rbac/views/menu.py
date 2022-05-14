# @Time : 2022/5/8 20:23 
# @Author : kongsh
# @File : menu.py
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.db.models import Q
from django.forms import formset_factory
from collections import OrderedDict

from rbac import models
from rbac.forms.permissions import MenuModelForm, PermissionModelForm
from rbac.forms.permissions import MultiPermissionForm
from rbac.service.routes import get_all_url_dict


def menu_list(request):
    """菜单列表"""
    menu_queryset = models.Menu.objects.all()
    mid = request.GET.get('mid', 0)
    # ##########显示所有的url及其归属的菜单【2.0】
    # #######方式一：通过3次sql查询完成，效率比较低
    # root_permission_list = []
    # if mid:
    #     # 找到指定菜单 + 其下可以成为菜单的权限
    #     permissions = models.Permission.objects.filter(menu_id=mid).order_by('-id')
    # else:
    #     # 找到所有可以成为菜单的权限
    #     permissions = models.Permission.objects.filter(menu__isnull=False).order_by('-id')
    # root_permission_queryset = permissions.values("id", 'title', 'url', 'alias', 'menu__title')
    # root_permission_dict = {}
    # for item in root_permission_queryset:
    #     item['children'] = []
    #     root_permission_list.append(item)
    #     root_permission_dict[item['id']] = item
    #
    # # 找到可以成为菜单的权限的所有子权限
    # node_permission_list = models.Permission.objects.filter(parent__in=permissions)\
    #                     .order_by('-id').values("id", 'title', 'url', 'alias', 'parent')
    #
    # for node in node_permission_list:
    #     parent = node['parent']
    #     root_permission_dict[parent]['children'].append(node)

    # #######方式二：拿到所有的权限，在python中组织好数据结构
    root_permission_dict = {}
    root_permission_list = []
    if mid:
        # 找到指定菜单 + 其下可以成为菜单的权限
        # permissions = models.Permission.objects.filter(menu_id=mid).order_by('-id')
        permissions = models.Permission.objects.filter(Q(menu_id=mid) | Q(parent__menu_id=mid)).order_by('-id')
    else:
        # 找到所有的权限
        permissions = models.Permission.objects.all().order_by('-id')
    root_permission_queryset = permissions.values("id", 'title', 'url', 'alias', 'menu__title', 'parent')
    for item in root_permission_queryset:
        if not item['parent']:
            # 找到所有能成为菜单的权限
            root_permission_dict[item['id']] = {
                'id': item['id'],
                'title': item['title'],
                'url': item['url'],
                'alias': item['alias'],
                'menu__title': item['menu__title'],
                'children': [],
            }

    for item in root_permission_queryset:
        if item['parent']:
            # 找到不能成为菜单的权限
            root_permission_dict[item['parent']]['children'].append({
                'id': item['id'],
                'title': item['title'],
                'url': item['url'],
                'alias': item['alias'],
                'menu__title': item['menu__title'],
            })

    root_permission_list = root_permission_dict.values()
    # #######方式二：END

    return render(request, 'rbac/menu_list.html', {
        'menu_queryset': menu_queryset,
        'root_permission_list': root_permission_list,
        'mid': mid
    })

    # ##########简单版本，只显示二级菜单【1.0】
    # permission_queryset = []
    # if mid:
    #     permission_queryset = models.Permission.objects.filter(menu_id=mid)
    # return render(request, 'rbac/menu_list.html',
    #               {'menu_queryset': menu_queryset,
    #                'permission_queryset': permission_queryset,
    #                'mid': mid,
    #                })


def menu_add(request):
    """添加菜单"""
    if request.method == "GET":
        form = MenuModelForm()
    else:
        form = MenuModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:menu_list'))
    return render(request, 'rbac/menu_add_edit.html', {'form': form})


def menu_edit(request, mid):
    """
    编辑菜单
    :param request:
    :param mid:
    :return:
    """
    obj = models.Menu.objects.filter(id=mid).first()
    if not obj:
        return HttpResponse('操作的菜单不存在')
    if request.method == "GET":
        form = MenuModelForm(instance=obj)
    else:
        form = MenuModelForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:menu_list'))
    return render(request, 'rbac/menu_add_edit.html', {'form': form})


def menu_del(request, mid):
    """
    删除菜单
    :param request:
    :param mid: 菜单id
    :return:
    """
    models.Menu.objects.filter(id=mid).delete()
    return redirect(reverse('rbac:menu_list'))


def permission_add(request):
    """
    添加权限
    :param request:
    :return:
    """
    if request.method == "GET":
        form = PermissionModelForm()
    else:
        form = PermissionModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:menu_list'))

    return render(request, 'rbac/permission_change.html',
                  {'form': form})


def permission_edit(request, pk):
    """
    编辑权限
    :param request:
    :param pk:
    :return:
    """
    obj = models.Permission.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse("权限不存在")
    if request.method == "GET":
        form = PermissionModelForm(instance=obj)
    else:
        form = PermissionModelForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:menu_list'))
    return render(request, 'rbac/permission_change.html', {'form': form})


def permission_del(request, pk):
    """
    删除权限
    :param request:
    :param pk:
    :return:
    """
    models.Permission.objects.filter(id=pk).delete()
    # 返回之前请求的url
    return redirect(request.META['HTTP_REFERER'])


def multi_permissions(request):
    """
    批量操作权限：数据库中的权限和路由系统中的权限进行对比，分析出需要增加，或者删除的权限
    :param request:
    :return:
    """
    generate_formset = None
    update_formset = None

    multi_permission_formset = formset_factory(MultiPermissionForm, extra=0)
    post_type = request.GET.get('type')
    if request.method == "POST":
        formset = multi_permission_formset(request.POST)
        # print('***************is_valid', formset.is_valid(), formset.errors)
        if formset.is_valid():
            for row_dict in formset.cleaned_data:
                permission_id = row_dict.pop('id')
                if post_type == 'generate':
                    # 新建
                    # print('***************row_dict', row_dict)
                    models.Permission.objects.create(**row_dict)
                elif post_type == 'update':
                    # 更新
                    models.Permission.objects.filter(id=permission_id).update(**row_dict)
        else:
            if post_type == 'generate':
                # 新建
                generate_formset = formset
            elif post_type == 'update':
                update_formset = formset

    # 1.数据库中获取所有的权限
    db_permissions = models.Permission.objects.all()\
        .values('id', 'title', 'url', 'alias', 'menu_id', 'parent_id')
    db_permisssion_dict = OrderedDict()
    for per in db_permissions:
        db_permisssion_dict[per['alias']] = per

    # 1.1数据库中所有权限的name集合
    db_permission_name_set = set(db_permisssion_dict.keys())

    # 2.1获取路由系统中所有的name集合
    router_dict = get_all_url_dict(ignore_namespace_list=['admin'])
    # print("***********获取路由系统中所有的name集合")
    # for k, v in router_dict.items():
    #     print(k, v)
    for row in db_permissions:
        alias = row['alias']
        if alias in router_dict:
            router_dict[alias].update(row)

    router_name_set = set(router_dict.keys())

    # 3.集合比较
    # 需要新建：数据库无、路由有
    # get请求或校验失败
    if not generate_formset:
        generate_name_list = router_name_set - db_permission_name_set
        generate_formset = multi_permission_formset(
            initial=[row for name, row in router_dict.items() if name in generate_name_list])
    # print('**************generate_formset"', generate_formset)
    # print("***********需要新建：数据库无、路由有")
    # for k in generate_name_list:
    #     print(k)
    # 需要删除：数据库有、路由无
    destory_name_list = db_permission_name_set - router_name_set
    destroy_formset = multi_permission_formset(
            initial=[row for name, row in db_permisssion_dict.items() if name in destory_name_list])

    # 需要更新：数据库有、路由有
    if not update_formset:
        update_name_list = db_permission_name_set.intersection(router_name_set)
        update_formset = multi_permission_formset(
            initial=[row for name, row in router_dict.items() if name in update_name_list])

    return render(
        request,
        'rbac/multi_permissions.html',
        {
            'destroy_formset': destroy_formset,
            'update_formset': update_formset,
            'generate_formset': generate_formset,
        }
    )

