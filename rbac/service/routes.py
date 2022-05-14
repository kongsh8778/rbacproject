# @Time : 2022/5/14 11:15 
# @Author : kongsh
# @File : routes.py
from django.conf import settings
from django.utils.module_loading import import_string
from django.urls.resolvers import URLResolver, URLPattern
from collections import OrderedDict


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    """
    递归获取所有的url
    :param pre_namespace:
    :param pre_url:
    :param urlpatterns:
    :param url_ordered_dict:
    :return:
    """
    for item in urlpatterns:
        if isinstance(item, URLResolver):
            if pre_namespace:
                if item.namespace:
                    namespace = "%s:%s" % (pre_namespace, item.namespace,)
                else:
                    namespace = pre_namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None
            # print(item.pattern.regex.pattern)
            recursion_urls(namespace, pre_url + item.pattern.regex.pattern,
                           item.url_patterns, url_ordered_dict)
        else:
            if pre_namespace:
                name = "%s:%s" % (pre_namespace, item.name,)
            else:
                name = item.name
            if not item.name:
                raise Exception('URL路由中必须设置name属性')

            url = pre_url + item.pattern.regex.pattern
            url_ordered_dict[name] = {'name': name,
                                      'url': url.replace('^', '').replace('$', '').replace('\\', '')}


def get_all_url_dict(ignore_namespace_list=None):
    """
    获取路由系统中所有的url
    :param ignore_namespace_list: 需要忽略的命名空间
    :return:
    """
    ignore_list = ignore_namespace_list or []
    url_ordered_dict = OrderedDict()

    md = import_string(settings.ROOT_URLCONF)
    urlpatterns = []
    for item in md.urlpatterns:
        if item.namespace in ignore_list:
            continue
        urlpatterns.append(item)

    recursion_urls(None, "/", urlpatterns, url_ordered_dict)
    # for k, v in url_ordered_dict.items():
    #     print(k, ' : ', v)
    return url_ordered_dict