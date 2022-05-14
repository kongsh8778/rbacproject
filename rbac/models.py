from django.db import models


class Menu(models.Model):
    """菜单表"""
    title = models.CharField(verbose_name="菜单名称", max_length=32, unique=True)
    icon = models.CharField(max_length=32, verbose_name="图标")

    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    权限表，基于url
    """
    title = models.CharField(max_length=32, verbose_name="标题")
    url = models.CharField(max_length=200, verbose_name="包含正则的URL")
    # ####【version 4.0】：权限粒度控制到按钮
    alias = models.CharField(verbose_name="URL别名", max_length=32, unique=True)
    # ####【version 3.0】：非菜单权限的归属，点击url后其所属的二级菜单能展示
    parent = models.ForeignKey(to='self', verbose_name="父权限", null=True,
                               blank=True, on_delete=models.CASCADE,
                               limit_choices_to={'parent__isnull': True})

    # ####【version 2.0】：动态生成二级菜单
    menu = models.ForeignKey(to='Menu', verbose_name="菜单", null=True,
                             blank=True, on_delete=models.CASCADE)

    # #########【version 1.0】：只有固定的一级菜单
    # is_menu = models.BooleanField(verbose_name="是否可做菜单", default=False)
    # icon = models.CharField(verbose_name='图标', null=True, blank=True, max_length=32)

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    角色表
    """
    title = models.CharField(max_length=32, verbose_name="角色名称")
    permissions = models.ManyToManyField(to=Permission, verbose_name="拥有的权限", blank=True)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """
    用户表
    """
    name = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(max_length=32, verbose_name="密码")
    roles = models.ManyToManyField(to='Role', verbose_name="拥有的角色", blank=True)

    def __str__(self):
        return self.name