from mangepicfudan import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import urlencode
from pathlib import PurePath,Path
import os

# Create your models here.
    

# class Doctor(models.Model):
# #   name = models.CharField(max_length=255,verbose_name="医生姓名")
# #   iddentificationID = models.CharField(max_length=255,unique=True,verbose_name="医生身份证")
# #   created_at = models.DateTimeField(auto_now_add=True,verbose_name="医生建档时间")
#   user = models.OneToOneField(User, on_delete=models.CASCADE)
#   def __str__(self) -> str:
#         return f"{self.user.username}-{self.user.first_name}{self.user.last_name}"
#   class Meta:
#         verbose_name = '医生'
#         verbose_name_plural = '医生集'

class Patient(models.Model):
  
  name = models.CharField(max_length=255,verbose_name="患者姓名")
  sex = models.CharField(max_length=255,verbose_name="性别")
  age = models.CharField(max_length=255,blank=True,null=True,verbose_name="年龄")
  receiveDate = models.DateField(verbose_name="收到日期")
  reportDate = models.DateField(verbose_name="报告日期")
  sampleNumber = models.CharField(max_length=255,blank=True,null=True,verbose_name="标本号")
  hospital = models.CharField(max_length=255,blank=True,null=True,verbose_name="送检医院")
  roomNumber = models.CharField(max_length=255,blank=True,null=True,verbose_name="病房")
  bedNumber = models.CharField(max_length=255,blank=True,null=True,verbose_name="病床")
  admissionNumber = models.CharField(max_length=255,blank=True,null=True,verbose_name="住院号")
  doctors = models.ManyToManyField(User,verbose_name="诊断医生", related_name='+')
  microscopy = models.TextField(verbose_name="镜检")
  advice = models.TextField(verbose_name="意见")

  creator = models.ForeignKey(User,verbose_name="记录创建者",on_delete=models.PROTECT, related_name='+')

        
  def __str__(self) -> str:
        return f"{self.name}"
  class Meta:
        verbose_name = '患者'
        verbose_name_plural = '患者集'

class  PathologyPictureItem(models.Model):
      pathologyPicture = models.ImageField(blank=True,null=True,upload_to=settings.images,verbose_name="肝穿图片",help_text="size < 1G的图片")
      bigPathologyPicture = models.FileField(blank=True,null=True,upload_to=settings.images,verbose_name="大肝穿图片",help_text="size >= 1G的图片或无法正常显示的图片")
      createdAt = models.DateTimeField(auto_now_add=True,verbose_name="图片上传时间")
      patient = models.ForeignKey(Patient, on_delete=models.CASCADE,verbose_name="患者")
      description = models.TextField(blank=True,null=True,verbose_name="图片描述")
      def __init__(self, *args, **kwargs):
            super(PathologyPictureItem, self).__init__(*args, **kwargs)

      class Meta:
            verbose_name = '肝穿图片'
            verbose_name_plural = '肝穿图片集'
      def __str__(self) -> str:
            return f"{self.patient.name}的编号为{self.id}的图片"