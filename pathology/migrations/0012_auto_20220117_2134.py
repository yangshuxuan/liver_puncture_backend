# Generated by Django 3.2.5 on 2022-01-17 13:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pathology', '0011_auto_20220117_1613'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='patient',
            options={'verbose_name': '患者', 'verbose_name_plural': '患者集'},
        ),
        migrations.AddField(
            model_name='patient',
            name='reportDate',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='报告日期'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='patient',
            name='name',
            field=models.CharField(max_length=255, verbose_name='患者姓名'),
        ),
    ]