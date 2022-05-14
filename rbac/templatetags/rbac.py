# @Time : 2022/5/3 16:58 
# @Author : kongsh
# @File : rbac.py
from django.template import Library
from django.conf import settings
from collections import OrderedDict
import re


register = Library()


@register.inclusion_tag("rbac/menu.html")
def menu(request):
    """
    生成动态菜单
    :param request:
    :return:
    """
    menu_dict = request.session.get(settings.MENU_SESSION_KEY, {})
    # print(menu_dict)
    order_dict = OrderedDict()

    for key in sorted(menu_dict):
        order_dict[key] = menu_dict[key]
        # 默认所有的二级菜单都是隐藏的
        menu_dict[key]['class'] = 'hide'

        for node in menu_dict[key]['child']:
            if request.current_menu_id == node['id']:
                node['class'] = 'active'
                menu_dict[key]['class'] = ''
            # ####【version 2.0】:通过url判断是否需要选中
            # reg = '^%s$' % node['url']
            # if re.match(reg, request.path_info):
            #     node['class'] = 'active'
            #     menu_dict[key]['class'] = ''

    return {'menu_dict': order_dict}


@register.inclusion_tag("rbac/breadcrumb.html")
def breadcrumb(request):
    return {'breadcrumb_list': request.breadcrumb_list}


@register.filter
def has_permission(request, name):
    """判断是否有别名的权限"""
    if name in request.session[settings.PERMISSION_SESSION_KEY]:
        return True
    return False
