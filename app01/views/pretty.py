from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm, PrettyEditModelForm, PrettyModelForm


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