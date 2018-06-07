"""qr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from qrcodes import views

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^add$', views.add),
    url(r'^vote/(?P<pk>[0-9]+)$', views.vote_view),
    url(r'^qr/(?P<pk>[0-9]+).png$', views.qr_view),
    url(r'^print/(?P<pk>[0-9]+)$', views.print_view),
    url(r'^vote/(?P<pk>[0-9]+)/(?P<vote>[1-3]+)$', views.vote_done_view),
    url(r'^info/(?P<pk>[0-9]+)$', views.info_view),
]
