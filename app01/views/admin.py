from django.shortcuts import render

from app01 import models
from app01.utils.pagination import Pagination

def admin_list(request):
    """ 管理员列表 """

    # 搜索
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["username__contains"] = search_data

    # 根据搜索条件去数据库获取
    queryset = models.PrettyNum.objects.filter(**data_dict)

    # 分页
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
        "search_data": search_data,
    }
    return render(request, 'admin_list.html', context)