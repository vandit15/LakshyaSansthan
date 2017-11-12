"""LakshyaSansthan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login
from LS.views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^$', home, name='home'),
	url(r'^ec/$', ec, name='ec'),
	url(r'^medical/$', medical, name='medical'),
	url(r'^news/$', news, name='news'),
	url(r'^subjects/$', subjects, name='subjects'),
	url(r'^teaching/$', teaching, name='teaching'),
	url(r'^login/$', login, name='login'),	
	url(r'^donate/$', donate, name='donate'),
	url(r'^dashboard/$', dashboard, name='dashboard'),	
	url(r'^register/$', register, name='register'),
	url(r'^logout/$', logout, name='logout'),
	url(r'^student/$', admin_student, name='student'),
	url(r'^view_student/$', view_student, name='view_student'),
	url(r'^nsf/$', admin_nsf, name='nsf'),
]
