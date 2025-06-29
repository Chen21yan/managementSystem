from django.shortcuts import render, redirect
from app01 import models
from app01.models import PrettyNum
from django.utils.safestring import mark_safe
from app01.utils.pagination import Pagination


# Create your views here.
def depart_list(request):
    """ 部门列表 """

    # 去数据库中获取所有的部门列表
    #  [对象,对象,对象]
    queryset = models.Department.objects.all()

    return render(request, 'depart_list.html', {'queryset': queryset})


def depart_add(request):
    """ 添加部门 """
    if request.method == 'GET':
        return render(request, 'depart_add.html')

    # 获取用户POST提交过来的数据（title输入为空）
    title = request.POST.get('title')

    # 保存到数据库
    models.Department.objects.create(title=title)

    # 重定向回部门列表
    return redirect('/depart/list')


def depart_delete(request):
    """ 删除部门 """
    # 获取ID http://127.0.0.1:8000/depart/delete/?nid=1
    nid = request.GET.get('nid')

    # 删除
    models.Department.objects.filter(id=nid).delete()

    # 跳转回
    # 重定向回部门列表
    return redirect('/depart/list')


def depart_edit(request, nid):
    """ 修改部门 """
    if request.method == 'GET':
        # 根据nid，获取其他的数据
        row_object = models.Department.objects.filter(id=nid).first()

        # print(row_object.id, row_object.title)

        return render(request, 'depart_edit.html', {"row_object": row_object})

    # 获取用户提交的标题
    title = request.POST.get('title')

    # 根据ID找到数据库中的数据并进行更新
    models.Department.objects.filter(id=nid).update(title=title)

    # 重定向回部门列表
    return redirect('/depart/list')


def user_list(request):
    """ 用户管理 """

    # 获取所有用户列表 [obj,obj,obj]
    queryset = models.UserInfo.objects.all()
    # for obj in queryset:
    #     print(obj.id, obj.name, obj.account, obj.create_time.strftime("%Y-%m-%d"), obj.gender, obj.get_gender_display(), obj.depart_id, obj.depart.title)
    #     # print(obj.name, obj.depart_id)
    #     # obj.depart_id  # 获取数据库中存储的那个字段值
    #
    #     # xx = models.Department.objects.filter(id=obj.depart_id).first()
    #     # xx.title
    #     # obj.depart.title  # 根据id自动去关联的表中获取哪一行数据depart对象。

    return render(request, 'user_list.html', {"queryset": queryset})


def user_add(request):
    """ 添加用户(原始方式) """

    if request.method == 'GET':
        # gender_choices 是静态定义，depart_list 是动态查询
        # 前者在代码中定义，后者在数据库存储
        # 前者适合不变的选择项，后者适合需要频繁变化的数据
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all()
        }
        return render(request, 'user_add.html', context)

    # 获取用户提交的数据
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('ac')
    ctime = request.POST.get('ctime')
    gender = request.POST.get('gd')
    depart_id = request.POST.get('dp')

    # 添加到数据库中
    models.UserInfo.objects.create(name=user, password=pwd, age=age,
                                   account=account, create_time=ctime,
                                   gender=gender, depart_id=depart_id)

    # 返回到用户列表页面
    return redirect("/user/list/")


# #################### ModelForm 示例 ####################
from django import forms

class UserModelForm(forms.ModelForm):
    # 用于创建一个文本输入框，并对用户输入进行基本验证。
    name = forms.CharField(min_length=3, label="用户名")

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", 'account', 'create_time', "gender", "depart"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        # }

    """
    *args 表示接收任意数量的位置参数（打包成元组 args）。
    **kwargs 表示接收任意数量的关键字参数（打包成字典 kwargs）。
    这种写法使得子类可以接受任意参数，而不需要明确声明所有可能的参数。
    """
    def __init__(self, *args, **kwargs):
        """
        super() 返回父类（超类）的代理对象，用于调用父类的方法。
        super().__init__(*args, **kwargs) 表示调用父类的 __init__ 方法，并将接收到的所有参数（*args 和 **kwargs）传递给父类。
        """
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class="form-control"
        for name, field in self.fields.items():
            # 可针对某些字段不加，进行判断
            # if name == "password":
            #     continue
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def user_model_form_add(request):
    """ 添加用户（ModelForm版本）"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {"form": form})

    # 用户POST提交数据，数据校验。
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        # {'name': 'cindy', 'password': '123', 'age': 21, 'account': Decimal('0'), 'create_time': datetime.datetime(2011, 11, 11, 0, 0, tzinfo=<UTC>), 'gender': 1, 'depart': <Department: 和平精英>}
        # print(form.cleaned_data)
        # 在 Django 中，form.save() 和 models.UserInfo.objects.create() 都可以用于创建新的数据库记录
        # models.UserInfo.objects.create(..)
        form.save()
        return redirect('/user/list/')

    # 校验失败（在页面上显示错误信息）
    return render(request, 'user_model_form_add.html', {"form": form})


def user_edit(request, nid):
    """ 编辑用户 """
    # 根据ID去数据库获取要编辑的那一行数据(对象)
    # models.UserInfo:表示访问 models.py 文件中定义的 UserInfo 模型类（对应数据库中的一个表）
    # .objects:是 Django 模型的默认管理器（Manager），用于数据库查询操作
    # .filter(): 查询方法，返回满足条件的查询集（QuerySet）
    #    id=nid: 查询条件，表示查找 id 字段等于 nid 变量值的记录
    #    相当于 SQL 中的 WHERE id = nid
    # .first():从查询结果中获取第一个对象（模型实例）,如果没有匹配结果则返回 None（而不会报错）
    row_object = models.UserInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要在用户输入以外增加一点值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {'form': form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


def pretty_list(request):
    """ 靓号列表 """

    # # 创建三百个数据
    # for i in range(300):
    #     models.PrettyNum.objects.create(mobile="18188888818", price=10, level=1, status=1)

    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["mobile__contains"] = search_data

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    page_object = Pagination(request, queryset, page_size=15)

    context = {'search_data': search_data,
               'queryset': page_object.page_queryset,   # 分完页的数据
               'page_string': page_object.html()        # 页码
    }
    return render(request, 'pretty_list.html', context)


    # # 搜索手机号方式一
    # q1 = models.PrettyNum.objects.filter(mobile="13945777890", id=3)
    # print(q1)
    #
    # # 搜索手机号方式二
    # data_dict = {"mobile":"13526789231", "id":2}
    # q2 = models.PrettyNum.objects.filter(**data_dict)
    # print(q2)


    # models.PrettyNum.objects.filter(id=3)      #等于3
    # models.PrettyNum.objects.filter(id__gt=3)   # 大于3
    # models.PrettyNum.objects.filter(id__gte=3)  # 大于等于3
    # models.PrettyNum.objects.filter(id__lt=3)   # 小于3
    # models.PrettyNum.objects.filter(id__lte=3)  # 小于等于3

    # models.PrettyNum.objects.filter(mobile__startswith="1399")   #筛选出以1399开头
    # models.PrettyNum.objects.filter(mobile__endswith="890")      #筛选出以890结尾
    # data_dict = {"mobile__contains": "999", "id__gt": 2}
    # q2 = models.PrettyNum.objects.filter(**data_dict)
    # models.PrettyNum.objects.filter(mobile__contains="999")      #筛选出包含999


from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
class PrettyModelForm(forms.ModelForm):
    # 验证方式1
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', "手机号格式错误")]
    )

    class Meta:
        model = models.PrettyNum
        # 自定义字段
        fields = ["mobile", "price", "level", "status"]
        # 排除某字段
        # exclude = ['level']
        # 所有
        # fields = "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    # 验证方式2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在！")
        return txt_mobile


def pretty_add(request):
    """ 添加靓号 """
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {'form': form})

    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_add.html', {'form': form})


class PrettyEditModelForm(forms.ModelForm):
    # mobile = forms.CharField(disabled=True, label="手机号") #显示出来，不可编辑

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_mobile(self):
        # 当前编辑的那一行ID
        # print(self.instance.pk)
        txt_mobile = self.cleaned_data['mobile']
        # 排除数据库中自己的这个手机号
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在！")
        return txt_mobile


def pretty_edit(request, nid):
    """ 编辑靓号 """
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_object)
        return render(request, 'pretty_edit.html', {'form': form})

    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_edit.html', {'form': form})


def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')