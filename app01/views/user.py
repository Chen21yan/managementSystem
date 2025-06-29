from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm, PrettyEditModelForm, PrettyModelForm


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

    page_object = Pagination(request, queryset, page_size=2)
    context = {'queryset': page_object.page_queryset,  # 分完页的数据
               'page_string': page_object.html()  # 页码
               }
    return render(request, 'user_list.html', context)


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