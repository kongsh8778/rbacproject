# @Time : 2022/5/8 16:40 
# @Author : kongsh
# @File : urls.py

from django.urls import path, re_path
from rbac.views import role
from rbac.views import menu


urlpatterns = [
    re_path(r'^role/list/$', role.role_list, name='role_list'),
    re_path(r'^role/add/$', role.role_add, name='role_add'),
    re_path(r'^role/edit/(?P<uid>\d+)$', role.role_edit, name='role_edit'),
    re_path(r'^role/del/(?P<uid>\d+)$', role.role_del, name='role_del'),

    re_path(r'^menu/list/$', menu.menu_list, name='menu_list'),
    re_path(r'^menu/add/$', menu.menu_add, name='menu_add'),
    re_path(r'^menu/edit/(?P<mid>\d+)$', menu.menu_edit, name='menu_edit'),
    re_path(r'^menu/del/(?P<mid>\d+)$', menu.menu_del, name='menu_del'),

    re_path(r'^permission/add/$', menu.permission_add, name='permission_add'),
    re_path(r'^permission/edit/(?P<pk>\d+)/$', menu.permission_edit, name='permission_edit'),
    re_path(r'^permission/del/(?P<pk>\d+)/$', menu.permission_del, name='permission_del'),
    re_path(r'^multi/permissions/$', menu.multi_permissions, name='multi_permissions'),

]
