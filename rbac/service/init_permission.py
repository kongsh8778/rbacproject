# @Time : 2022/5/3 16:28 
# @Author : kongsh
# @File : init_permission.py
from django.conf import settings


def init_permission(request, user):
    """
    登陆成功后初始化权限
    :param request:
    :param user:
    :return:
    """
    # values是左连接，会把空的也取出来
    permission_queryset = user.roles.filter(permissions__url__isnull=False)\
        .values('permissions__url',
                'permissions__title',
                'permissions__id',
                'permissions__alias',
                'permissions__parent_id',
                'permissions__menu__title',# 获取菜单的名称【version 2.0】
                'permissions__menu__icon',# 获取菜单的icon【version 2.0】
                # 'permissions__icon', # version 1.0
                # 'permissions__is_menu',# version 1.0
                ).distinct()

    menu_dict = {}
    # 存储所有的权限，用于权限验证
    permission_dict = {}
    for row in permission_queryset:
        # ####【version 5.0】：别名作为key
        permission_dict[row['permissions__alias']] = {
            'url': row['permissions__url'],
            'id': row['permissions__id'],
            'pid': row['permissions__parent_id'],
            'title': row['permissions__title'],
            'alias': row['permissions__alias'],
        }
        # # ####【version 4.0】：增加面包屑导航条
        # permission_dict[row['permissions__id']] = {
        #     'url': row['permissions__url'],
        #     'id': row['permissions__id'],
        #     'pid': row['permissions__parent_id'],
        #     'title': row['permissions__title'],
        # }

        # # ####【version 3.0】：非菜单权限的归属，点击url后其所属的二级菜单能展示
        # # permission_list.append({'permissions__url': row['permissions__url']})
        # permission_list.append({'url': row['permissions__url'],
        #                         'id': row['permissions__id'],
        #                         'pid': row['permissions__parent_id'],
        #                         })

        # #####【version 1.0】：只有固定的一级菜单

        # if row['permissions__is_menu']:
            # menu_list.append({
            #     'title': row['permissions__title'],
            #     'icon': row['permissions__icon'],
            #     'url': row['permissions__url']
            # })
        # ####【version 2.0】：动态生成二级菜单
        title = row.get('permissions__menu__title', '')
        # title为空，表示不需要用来生成菜单
        if not title:
            continue

        if title not in menu_dict:
            menu_dict[title] = {
                'title': row['permissions__menu__title'],
                'icon': row['permissions__menu__icon'],
                'child': [{'id': row['permissions__id'],
                           'url': row['permissions__url'],
                           'title': row['permissions__title'],
                           }]
                }
        else:
            menu_dict[title]['child'].append(
                {'id': row['permissions__id'],
                 'url': row['permissions__url'],
                 'title': row['permissions__title'],
                 }
            )

    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
    request.session[settings.MENU_SESSION_KEY] = menu_dict


