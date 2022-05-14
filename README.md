# rbacproject
# 一、作用：基于角色的用户访问控制，
可以动态生成菜单，批量权限处理

# 二、处理流程：
用户登陆成功后获取权限，并将用户拥有的【权限和菜单】信息写入到session中；后续用户访问时，在中间件进行权限校验。
在后台通过inclusion_tag动态生成二级菜单，将权限控制到按钮级别。

# 三、项目应用该组件流程
- 用户登陆：调用rbac组件中的init_permission方法，对菜单和权限进行初始化；
- 配置中间件：settings.py文件
![image](https://user-images.githubusercontent.com/48315749/168429273-275bd94e-546d-4d1f-966f-332974d3c7ac.png)
- 配置白名单：settings.py文件
![image](https://user-images.githubusercontent.com/48315749/168429288-24f10f48-6810-427c-b90c-6b772d2141e5.png)
- 配置session中使用的key：settings.py文件
![image](https://user-images.githubusercontent.com/48315749/168429301-8727fd13-8b70-4db8-a1ff-ce0cd3475948.png)

-load rbac:动态生成菜单和面包屑导航条
![image](https://user-images.githubusercontent.com/48315749/168429322-e681113f-da4c-4659-a5b6-d27ad11d1c70.png)
