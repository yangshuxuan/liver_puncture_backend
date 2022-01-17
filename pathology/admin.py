from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html,urlencode
from django.urls import reverse
from django.db.models import Q
from django.db.models.functions import Concat
from mangepicfudan.settings import STATIC_URL
from django.utils.safestring import mark_safe
import os
from . import models

admin.site.site_url = "/media/help.pdf"
class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.xml'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice
class DeadReasonFilter(InputFilter):
    parameter_name = 'deadReason'
    title = '死亡原因'

    def queryset(self, request, queryset):
        if self.value() is not None:
            deadReason = self.value()

            return queryset.filter(
                Q(deadReason__icontains=deadReason)
            )
class OperateDiagoseFilter(InputFilter):
    parameter_name = 'operateDiagose'
    title = '解剖诊断'

    def queryset(self, request, queryset):
        if self.value() is not None:
            operateDiagose = self.value()

            return queryset.filter(
                Q(operateDiagose__icontains=operateDiagose)
            )
class OperateSeqNumberFilter(InputFilter):
    parameter_name = 'operateSeqNumber'
    title = '剖验号数'

    def queryset(self, request, queryset):
        if self.value() is not None:
            operateSeqNumber = self.value()

            return queryset.filter(
                Q(operateSeqNumber__icontains=operateSeqNumber)
            )
class DoctorFullnameFilter(InputFilter):
    parameter_name = 'doctorFullname'
    title = '诊断医生'

    def queryset(self, request, queryset):
        if self.value() is not None:
            doctorFullname = self.value()
            u = User.objects.annotate(full_name=Concat('last_name','first_name')).filter(Q(full_name=doctorFullname)).values('id')

            return queryset.filter(
                Q(doctors__id__in=u)
            )


class PathologyPictureInline(admin.StackedInline):
    model = models.PathologyPictureItem
    extra = 0
@admin.register(models.Patient)
class PatientAdmin(admin.ModelAdmin):

    fieldsets = (
        ('患者基本信息', {
            'fields': (('name', 'sex'), 'age', ('roomNumber','bedNumber'),'admissionNumber',),

        }),
        ('报告基本信息', {
            'fields': (('sampleNumber', 'hospital'),'receiveDate','doctors'),

        }),
        ('诊断结果', {
            'fields': ( 'microscopy','advice','reportDate'),

        }),
        

    )
    filter_horizontal = (
        'doctors',
    )
    list_filter = (
        # OperateSeqNumberFilter,
        # OperateDiagoseFilter,
        # DeadReasonFilter,
        DoctorFullnameFilter,
    )
    list_display = ['name','sex','age','doctorNames','enterPictureList','generateDignoseDoc','receiveDate','reportDate','creatorFunc']
    inlines = [PathologyPictureInline]
    ordering = ['name']
    search_fields = ['name',
    'doctors__username',
    'doctors__first_name',
    'doctors__last_name','creator__username']
    
    exclude = ('creator',)
    list_per_page = 10
    always_show_username = True

    @admin.display(description="诊断报告")
    def generateDignoseDoc(self,patient):
        base_url = "/generatedoc"
        query_string =  urlencode({'patient__id': patient.id})  
        url = '{}?{}'.format(base_url, query_string)
        return format_html('<a href="{}"><img src="{}pathology/explorer.svg" width="25" height="20" alt="浏览"></a>',url,STATIC_URL)


    @admin.display(description="记录创建者")
    def creatorFunc(self,patient):
        return self.get_user_label(patient.creator) 
    
    @admin.display(description="诊断医生")
    def doctorNames(self,patient):
        return ",".join([ self.get_user_label(d) for d in list(patient.doctors.all())])
    
    @admin.display(description="肝穿图片列表")
    def enterPictureList(self,patient):
        if patient.pathologypictureitem_set.first():
            url = (reverse('admin:pathology_pathologypictureitem_changelist') 
            + "?" 
            + urlencode({'patient__id':str(patient.id)}))
            return format_html('<a href="{}"><img src="{}pathology/finger.svg" width="25" height="20" alt="浏览"></a>',url,STATIC_URL)
    
    
    
    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)
    
    def has_change_permission(self,request, obj=None):
        if obj is None:
            return True
        return obj.doctors.filter(id = request.user.id).exists()
    def has_delete_permission(self,request, obj=None):
        if obj is None:
            return True
        return obj.creator.id == request.user.id
    

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(PatientAdmin, self).formfield_for_foreignkey(
                                                db_field, request, **kwargs)
        if db_field.related_model == User:
            field.label_from_instance = self.get_user_label
        return field


    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "doctors":
            kwargs["queryset"] = User.objects.filter(groups__name='普通医生')
        # return super().formfield_for_manytomany(db_field, request, **kwargs)
        field = super(PatientAdmin, self).formfield_for_manytomany(
                                                db_field, request, **kwargs)
        if db_field.name == "doctors":
            field.label_from_instance = self.get_user_label
        return field

    def get_user_label(self, user):
        name = f"{user.last_name}{user.first_name}"
        # name = user.get_full_name()
        username = user.username
        if not self.always_show_username:
            return name or username
        return (name and name != username and '%s (%s)' % (name, username)
                or username)
        


@admin.register(models.PathologyPictureItem)
class PathologyPictureAdmin(admin.ModelAdmin):
    readonly_fields = ["headshot_big_image"]
    list_display = ['patient','createdAt','description','showBigPathologyPicture','showPathologyPicture','headshot_small_image']
    autocomplete_fields = ['patient']
    ordering = ['createdAt']
    list_per_page = 10
    @admin.display(description="肝穿图片链接")
    def showPathologyPicture(self,pathologyPictureItem):
        if pathologyPictureItem.pathologyPicture:
            return format_html('<a href="{}">{}</a>',pathologyPictureItem.pathologyPicture.url,os.path.basename(pathologyPictureItem.pathologyPicture.name))
        else:
            return None
    @admin.display(description="大肝穿图片链接")
    def showBigPathologyPicture(self,pathologyPictureItem):
        if pathologyPictureItem.bigPathologyPicture:
            return format_html('<a href="{}">{}</a>',pathologyPictureItem.bigPathologyPicture.url,os.path.basename(pathologyPictureItem.bigPathologyPicture.name))
        else:
            return None

    
    @admin.display(description="肝穿图片")
    def headshot_small_image(self, obj):
        width = 200
        if obj and obj.pathologyPicture  and obj.pathologyPicture.size <= 10 *1024 * 1024  :
            return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url = obj.pathologyPicture.url,
                width=width,
                height=1.0 * obj.pathologyPicture.height/obj.pathologyPicture.width * width,
            )
    )
    @admin.display(description="肝穿图片")
    def headshot_big_image(self, obj):
        width = 400
        if obj and obj.pathologyPicture  and obj.pathologyPicture.size <= 10 *1024 * 1024:
            return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url = obj.pathologyPicture.url,
                width=width,
                height=1.0 * obj.pathologyPicture.height/obj.pathologyPicture.width * width,
            )
    )
    
