"""mangepicfudan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from . import views
from . import settings
admin.site.site_header = "复旦大学医学院病理系肝穿工作站"
admin.site.site_title = "肝穿信息管理"
urlpatterns =[
    url(r'^%s(?P<path>.*)$' % settings.PPT_URL[1:], views.protected_serve, {'document_root': settings.PPT_ROOT}),
    url(r'^%s(?P<path>.*)$' % settings.RECORDS_URL[1:], views.protected_serve, {'document_root': settings.RECORDS_ROOT}),
    url(r'^%s(?P<path>.*)$' % settings.OTHERDOCS_URL[1:], views.protected_serve, {'document_root': settings.OTHERDOCS_ROOT}),
    url(r'^%s(?P<path>.*)$' % settings.IMAGES_URL[1:], views.protected_serve, {'document_root': settings.IMAGES_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path('generatedoc', views.generateDocument),
    path('', admin.site.urls),
]
