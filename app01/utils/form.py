from app01 import models
from django import forms
from app01.utils.bootstrap import BootStrapModelForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class UserModelForm(BootStrapModelForm):
    # 用于创建一个文本输入框，并对用户输入进行基本验证。
    name = forms.CharField(min_length=3,
                           label="用户名",
                           widget=forms.TextInput(attrs={'class': 'form-control'})
                           )

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", 'account', 'create_time', "gender", "depart"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        # }


class PrettyModelForm(BootStrapModelForm):
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

    # 验证方式2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在！")
        return txt_mobile


class PrettyEditModelForm(BootStrapModelForm):
    # mobile = forms.CharField(disabled=True, label="手机号") #显示出来，不可编辑

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]

    def clean_mobile(self):
        # 当前编辑的那一行ID
        # print(self.instance.pk)
        txt_mobile = self.cleaned_data['mobile']
        # 排除数据库中自己的这个手机号
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在！")
        return txt_mobile

