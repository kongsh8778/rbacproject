# @Time : 2022/5/3 16:12 
# @Author : kongsh
# @File : rbac.py
# 权限控制中间件

from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import redirect, HttpResponse, reverse
import re


class RbacMiddleware(MiddlewareMixin):
    """
    权限控制中间件
    """
    def process_request(self, request):
        """
        权限控制
        :param request:
        :return:
        """
        # 1、获取当前请求的url
        current_url = request.path_info

        # 2、白名单处理
        for url_reg in settings.VALID_URL:
            if re.match(url_reg, current_url):
                return None
        # 3、获取当前用户session中的所有权限
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_dict:
            return redirect('/login/')

        request.breadcrumb_list = [
            {'title': "首页", 'url': "/"},
        ]
        # 4、验证是否有当前url的权限
        # print("***********permission_list:", permission_list)
        # print("***********current_url:", current_url)
        for item in permission_dict.values():
            # reg = '^%s$' % item['permissions__url']
            reg = '^%s$' % item['url']
            obj_id = item['id']
            pid = item['pid']
            alias = item['alias']
            if re.match(reg, current_url):
                if pid:
                    # 有父id，说明是普通url
                    request.current_menu_id = pid
                    request.breadcrumb_list.extend([
                        # {'title': permission_dict[str(pid)]['title'], 'url': permission_dict[str(pid)]['url']},
                        {'title': permission_dict[alias]['title'], 'url': permission_dict[alias]['url']},
                        {'title': item['title'], 'url': item['url']},
                    ])
                    # print('**********item', item)
                else:
                    # 没有父id，说明是菜单
                    request.current_menu_id = obj_id
                    request.breadcrumb_list.extend([
                        {'title': item['title'], 'url': item['url']},
                    ])
                break
        else:
            # return HttpResponse("无权访问")
            return redirect(reverse('login'))