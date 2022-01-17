# Generated by Django 3.2.5 on 2021-09-22 02:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='病人姓名')),
                ('sex', models.CharField(max_length=255, verbose_name='性别')),
                ('age', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='年龄')),
                ('iddentificationID', models.CharField(max_length=255, unique=True, verbose_name='病人身份证')),
                ('operateSeqNumber', models.CharField(max_length=255, unique=True, verbose_name='剖验号数')),
                ('deathDate', models.DateField(verbose_name='死亡时日')),
                ('operateDate', models.DateField(verbose_name='解剖时日')),
                ('operateDiagose', models.TextField(verbose_name='解剖诊断')),
                ('deadReason', models.TextField(verbose_name='死亡原因')),
                ('operateRecord', models.FileField(null=True, upload_to='records', verbose_name='解剖记录')),
                ('pptRecord', models.FileField(null=True, upload_to='ppt', verbose_name='PPT')),
                ('otherDocument', models.FileField(null=True, upload_to='otherdocs', verbose_name='其他文档')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='患者建档时间')),
                ('lastModifiedAt', models.DateTimeField(auto_now=True, verbose_name='最后修改时间')),
                ('otherDoctors', models.CharField(max_length=255, verbose_name='其他医生')),
                ('sliceNum', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='切片数')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='记录创建者')),
                ('doctors', models.ManyToManyField(related_name='_pathology_patient_doctors_+', to=settings.AUTH_USER_MODEL, verbose_name='剖验医生')),
            ],
            options={
                'verbose_name': '病人',
                'verbose_name_plural': '病人集',
            },
        ),
        migrations.CreateModel(
            name='PathologyPictureItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pathologyPicture', models.FileField(upload_to='images', verbose_name='病理图片')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='图片上传时间')),
                ('description', models.TextField(blank=True, null=True, verbose_name='图片描述')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pathology.patient', verbose_name='患者')),
            ],
            options={
                'verbose_name': '病理图片',
                'verbose_name_plural': '病理图片集',
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iddentificationID', models.CharField(max_length=255, unique=True, verbose_name='医生身份证')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '医生',
                'verbose_name_plural': '医生集',
            },
        ),
    ]