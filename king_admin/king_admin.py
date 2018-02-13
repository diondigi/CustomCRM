#!/usr/bin/python
#-*- coding: utf-8 -*-


'''
这里重写admin.将新的admin作为一个应用，便于扩展和移植。根目录下，创建应用，并命名为：king_admin.这里不显示原生后台的Users和Groups内容，
将在后面的权限管理中独立出来
'''
__author__ = 'fw'
from crm import models
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
#数据结构容器
enable_admin = {}
#{"crm":{"customer":"customerAdmin"}}
#admin.site.register(models.Customer,CustomerAdmin)

#覆写admin的起点，很重要，理解其实现思路
#构造数据结构--->通过models类和自定义类注册获取
def register(model_class,admin_class=None):
    #通过model中的类名来获取类对应的应用名
    app_name = model_class._meta.app_label
    if app_name not in enable_admin:
        #添加项目名称
        enable_admin[app_name] = {}
    table_name = model_class._meta.model_name
    #添加自定义类属性为models类
    admin_class.model = model_class
    #通过表名获取到自定义类
    enable_admin[app_name][table_name] = admin_class


#创建基类
class BaseAdmin(object):
    list_display = []
    list_filter = []
    # search_field = ["id"]
    #分页每页显示数据量
    list_per_page = 10
    #在前端以横向方式显示复选框
    filter_horizontal = []
    readonly_fields = []
    #设置表的只读属性
    readonly_table = False
    actions = {}
    modelform_exclude_fields = []

    #用户可以自定制表单自定制验证规则,用于对所有字段做循环验证，对应form中的clean方法
    def default_form_validation(self):
        pass

    def delete_multi_obj(self,request):
        pass




from django.shortcuts import HttpResponse, render,redirect
from django.utils.safestring import mark_safe
from king_admin import utils
#自定义类，显示特定字段
class CustomerAdmin(BaseAdmin):
    # 数据显示的字段 ,并且实现表中没有的自定制字段的显示,如enroll
    list_display = ["id","qq","name","source","status","consultant","consult_course","date","status","enroll"]
    # list_display = ["qq","name","source","referral_from","consultant","consult_course"]
    # 下拉列表框用于一对多、choice字段的过滤
    list_filter = ["source","consultant","consult_course","date"]
    #每页数据显示的条数
    list_per_page = 3
    #查询字段
    search_field = ["qq","name"]
    #显示多对多关系中的复选框
    filter_horizontal = ["tags"]

    #自定制下拉列表框中的动作函数
    actions = {"多行删除":"delete_multi_obj"}
    #只读字段
    readonly_fields = ["qq","consult_course"]
    #设置customer表为只读
    # readonly_table = True
    readonly_table = False

    #实现表中没有的自定制Field的显示功能，与tags.py中函数关联
    def enroll(self):
        #此处可以弹出一个页面，然后进行一下步操作
        #由于此方法在动态调用前，对self动态添加了两个属性request,obj_id
        request = self.request
        obj_id = self.row_id
        status = self.instance.status
        if status == 0:
            url = "<a href='/crm/customer/%s/enrollment/'>报名</a>"%obj_id
        else:
            url = "<a href='/crm/customer/%s/enrollment/'>报名新课程</a>" % obj_id
        return url
    #函数还可以点属性，太牛了。。。
    enroll.display_name = "报名链接"

    #多行删除函数
    def delete_multi_obj(self,request, querysets):
        html_content = ""
        table_name = self.model._meta.model_name
        app_name = self.model._meta.app_label
        ids = ",".join([str(obj.id) for obj in querysets])
        select_action = request.POST.get("select_action")

        for obj in querysets:
            html_content += utils.build_delete_obj_content_show(obj)
        if self.readonly_table:
            error = "Table is readonly,cannot be modifyed or added!"
        else:
            error = ""
        if "confirm_delete" in request.POST and not self.readonly_table:
            querysets.delete()
            return redirect(".")

        return render(request, "king_admin/delete_multi_table_obj.html",
                      {"html_content": mark_safe(html_content),
                       "app_name":app_name,"table_name":table_name,
                       "ids":ids,"select_action":select_action,
                       "error":error
                       })


    #用户自定制验证规则接口,此接口函数其实是在modeform表单进行数据验证时自动调用的
    #这里用户自定义form验证，相当于django框架中form的clean方法
    #以下例子是用来判断customer表中的content字段长度必须大于10,否则抛出异常然后在前台表单中的formobj.errors中显示
    def default_form_validation(modelform_obj):
        #后端对象
        backend_obj = modelform_obj.instance
        #前端POST提交的字典数据
        forward_obj = modelform_obj.cleaned_data
        content_field_val = forward_obj.get("content")
        if content_field_val:
           if len(content_field_val) <=10:
               # raise ValidationError(
               #     _("Field %(field)s length is short,it shoud be more than %(len)s"),
               #     code="invaild",
               #     params={"field": "content", "len": "10" }
               # )
               #不在king_admin.py中进行异常的抛出，而是将异常对象返回给调用方 forms.py
                return modelform_obj.ValidationError(
                   _("Field %(field)s length is short,it shoud be more than %(len)s"),
                   code="invaild",
                   params={"field": "content", "len": "10" }
               )

    #自定制单个字段的验证规则，抛出的错误会在template模板中"字段.errors.0"显示
    #具体验证逻辑在form.py中
    def clean_name(modelform_obj):
        field_name_val = modelform_obj.cleaned_data.get("name")
        print("field_name_val:",field_name_val)
        #if not None
        if not field_name_val:
            modelform_obj.add_error("name","字段不能为空")
        else:
            return field_name_val



class UserProfileAdmin(BaseAdmin):
    list_display = ["email","name"]
    readonly_fields = ["password"]
    #在此主要排除系统自动维护的时间字段，因为这些字段不需要我们维护和添加
    modelform_exclude_fields = ["last_login"]
    #作用在多对多关系上
    filter_horizontal = ["user_permissions","groups","roles"]




class TagAdmin(BaseAdmin):
    pass

class CourseAdmin(BaseAdmin):
    pass

class BranchAdmin(BaseAdmin):
    pass

class ClassListAdmin(BaseAdmin):
    pass

class CourseRecordAdmin(BaseAdmin):
    list_display = ("from_class", "day_num", "teacher", "has_homework")
    # 下拉列表框用于一对多、choice字段的过滤
    list_filter = ["from_class"]
    #查询字段
    search_field = ["from_class"]

    # 自定制下拉列表框中的动作函数
    actions = {"初始化学生上课纪录": "initialize_student_record"}

    def initialize_student_record(modeladmin, request, queryset):
        if len(queryset) >1:
            return HttpResponse("只能选择一个班级")

        courserecord_obj = queryset[0]

        #创建方式一：普通的单行记录依次创建，在大数据下效率低
        # for enroll_obj in courserecord_obj.from_class.enrollment_set.all():
        #     #get_or_create表示如果存在就不创建，如果不存在就创建
        #     models.StudyRecord.objects.get_or_create(student=enroll_obj,
        #                                              course_record=courserecord_obj,score=0)

        #创建方式二：批量创建，效率高，支持事务
        studyrecord_objs = []
        for enroll_obj in courserecord_obj.from_class.enrollment_set.all():
            studyrecord_obj = models.StudyRecord(student=enroll_obj,course_record=courserecord_obj,score=0)
            studyrecord_objs.append(studyrecord_obj)
        #先删除后创建
        # models.StudyRecord.objects.filter(course_record=courserecord_obj).delete()
        try:
            models.StudyRecord.objects.bulk_create(studyrecord_objs)
        except Exception as e:
            print("数据已经存在:",e)

        return redirect("../studyrecord")


class StudyRecordAdmin(BaseAdmin):
    pass
class EnrollmentAdmin(BaseAdmin):
    pass

class PaymentAdmin(BaseAdmin):
    pass

class CustomerFollowUpAdmin(BaseAdmin):
    pass
class RoleAdmin(BaseAdmin):
    pass

class MenuAdmin(BaseAdmin):
    pass

class ContractAdmin(BranchAdmin):
    pass

#进行注册，构造数据结构
register(models.Contract,ContractAdmin)
register(models.Customer,CustomerAdmin)

register(models.UserProfile,UserProfileAdmin)
register(models.Tag,TagAdmin)
register(models.Course,CourseAdmin)
register(models.Branch,BranchAdmin)
register(models.ClassList,ClassListAdmin)
register(models.CourseRecord,CourseRecordAdmin)
register(models.StudyRecord,StudyRecordAdmin)
register(models.Enrollment,EnrollmentAdmin)
register(models.Payment,PaymentAdmin)
register(models.CustomerFollowUp,CustomerFollowUpAdmin)
register(models.Role,RoleAdmin)
register(models.Menu,MenuAdmin)
