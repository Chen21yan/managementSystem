from django.shortcuts import render

# Create your views here.
def depart_list(request):
    """ 部门列表 """
    return render(request, 'depart_list.html')