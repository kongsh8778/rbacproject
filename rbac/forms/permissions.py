# @Time : 2022/5/8 17:45 
# @Author : kongsh
# @File : permissions.py
from django import forms
from rbac import models
from django.utils.safestring import mark_safe


class RoleModelForm(forms.ModelForm):
    """角色的modelform"""
    class Meta:
        model = models.Role
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }


ICON_LIST = [
    ['fa-address-book', '<i aria-hidden="true" class="fa fa-address-book"></i>'],
    ['fa-address-book-o', '<i aria-hidden="true" class="fa fa-address-book-o"></i>'],
    ['fa-address-card', '<i aria-hidden="true" class="fa fa-address-card"></i>'],
    ['fa-address-card-o', '<i aria-hidden="true" class="fa fa-address-card-o"></i>'],
    ['fa-adjust', '<i aria-hidden="true" class="fa fa-adjust"></i>'],
    ['fa-american-sign-language-interpreting',
     '<i aria-hidden="true" class="fa fa-american-sign-language-interpreting"></i>'],
    ['fa-anchor', '<i aria-hidden="true" class="fa fa-anchor"></i>'],
    ['fa-archive', '<i aria-hidden="true" class="fa fa-archive"></i>'],
    ['fa-area-chart', '<i aria-hidden="true" class="fa fa-area-chart"></i>'],
    ['fa-arrows', '<i aria-hidden="true" class="fa fa-arrows"></i>'],
    ['fa-arrows-h', '<i aria-hidden="true" class="fa fa-arrows-h"></i>'],
    ['fa-arrows-v', '<i aria-hidden="true" class="fa fa-arrows-v"></i>'],
    ['fa-asl-interpreting', '<i aria-hidden="true" class="fa fa-asl-interpreting"></i>'],
    ['fa-assistive-listening-systems', '<i aria-hidden="true" class="fa fa-assistive-listening-systems"></i>'],
    ['fa-asterisk', '<i aria-hidden="true" class="fa fa-asterisk"></i>'],
    ['fa-at', '<i aria-hidden="true" class="fa fa-at"></i>'],
    ['fa-audio-description', '<i aria-hidden="true" class="fa fa-audio-description"></i>'],
    ['fa-automobile', '<i aria-hidden="true" class="fa fa-automobile"></i>'],
    ['fa-balance-scale', '<i aria-hidden="true" class="fa fa-balance-scale"></i>'],
    ['fa-ban', '<i aria-hidden="true" class="fa fa-ban"></i>'],
    ['fa-bank', '<i aria-hidden="true" class="fa fa-bank"></i>'],
    ['fa-bar-chart', '<i aria-hidden="true" class="fa fa-bar-chart"></i>'],
    ['fa-bar-chart-o', '<i aria-hidden="true" class="fa fa-bar-chart-o"></i>'],
    ['fa-barcode', '<i aria-hidden="true" class="fa fa-barcode"></i>'],
    ['fa-bars', '<i aria-hidden="true" class="fa fa-bars"></i>'],
    ['fa-bath', '<i aria-hidden="true" class="fa fa-bath"></i>'],
    ['fa-bathtub', '<i aria-hidden="true" class="fa fa-bathtub"></i>'],
    ['fa-battery', '<i aria-hidden="true" class="fa fa-battery"></i>'],
    ['fa-battery-0', '<i aria-hidden="true" class="fa fa-battery-0"></i>'],
    # ['fa-battery-1', '<i aria-hidden="true" class="fa fa-battery-1"></i>'],
    # ['fa-battery-2', '<i aria-hidden="true" class="fa fa-battery-2"></i>'],
    # ['fa-battery-3', '<i aria-hidden="true" class="fa fa-battery-3"></i>'],
    # ['fa-battery-4', '<i aria-hidden="true" class="fa fa-battery-4"></i>'],
    # ['fa-battery-empty', '<i aria-hidden="true" class="fa fa-battery-empty"></i>'],
    # ['fa-battery-full', '<i aria-hidden="true" class="fa fa-battery-full"></i>'],
    # ['fa-battery-half', '<i aria-hidden="true" class="fa fa-battery-half"></i>'],
    # ['fa-battery-quarter', '<i aria-hidden="true" class="fa fa-battery-quarter"></i>'],
    # ['fa-battery-three-quarters', '<i aria-hidden="true" class="fa fa-battery-three-quarters"></i>'],
    ['fa-bed', '<i aria-hidden="true" class="fa fa-bed"></i>'],
    # ['fa-beer', '<i aria-hidden="true" class="fa fa-beer"></i>'],
    ['fa-bell', '<i aria-hidden="true" class="fa fa-bell"></i>'],
    # ['fa-bell-o', '<i aria-hidden="true" class="fa fa-bell-o"></i>'],
    # ['fa-bell-slash', '<i aria-hidden="true" class="fa fa-bell-slash"></i>'],
    # ['fa-bell-slash-o', '<i aria-hidden="true" class="fa fa-bell-slash-o"></i>'],
    ['fa-bicycle', '<i aria-hidden="true" class="fa fa-bicycle"></i>'],
]
for item in ICON_LIST:
    item[1] = mark_safe(item[1])


class MenuModelForm(forms.ModelForm):
    """
    菜单的modelform
    """
    class Meta:
        model = models.Menu
        fields = ['title', 'icon']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "请输入菜单名称"}),
            'icon': forms.RadioSelect(choices=ICON_LIST),
        }
        error_messages = {
            'title': {'required': '菜单名称不能为空'},
            'icon': {'required': '图标不能为空'},
        }


class PermissionModelForm(forms.ModelForm):
    """权限表对应的modelform"""
    class Meta:
        model = models.Permission
        fields = "__all__"
        help_texts = {
            'parent': "父级权限，无法作为菜单的权限才需要选择",
            'menu': "选中表示该权限可以作为菜单；否则不可做菜单"
        }

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '请输入权限名称'}),
            'url': forms.TextInput(attrs={'placeholder': '请输入URL'}),
            'alias': forms.TextInput(attrs={'placeholder': '请输入URL别名'}),
            'parent': forms.Select(attrs={'placeholder': '请选择父级权限'}),
            'menu': forms.Select(attrs={'placeholder': '请选择菜单'}),
        }

        error_messages = {
            'title': {'required': '权限名不能为空', },
            'url': {'required': 'URL不能为空', },
            'alias': {'required': 'URL别名不能为空', },
        }

    def __init__(self, *args, **kwargs):
        """初始化函数"""
        super().__init__(*args, **kwargs)
        # 所有字段批量增加form-control属性
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-control"})

    def clean(self):
        """g钩子函数"""
        menu = self.cleaned_data.get('menu')
        parent = self.cleaned_data.get('parent')
        if menu and parent:
            self.add_error('menu', '菜单和根权限不能同时存在')


class MultiPermissionForm(forms.Form):
    """
    批量操作的form
    """
    # id = forms.IntegerField(widget=forms.HiddenInput, required=True)
    id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                            required=False)
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    alias = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    menu_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )
    parent_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': "form-control"}),
        required=False,
    )
    error_messages = {
        'title': {'required': '权限名不能为空',}
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
        self.fields['parent_id'].choices += models.Permission.objects.filter(parent__isnull=True).exclude(
            menu__isnull=True).values_list('id', 'title')

    def clean_pid_id(self):
        menu = self.cleaned_data.get('menu_id')
        pid = self.cleaned_data.get('parent_id')
        if menu and pid:
            raise forms.ValidationError('菜单和根权限同时只能选择一个')
        return pid
