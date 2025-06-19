from django.shortcuts import render, redirect
from app01 import models

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