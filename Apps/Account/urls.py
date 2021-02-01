"""BillingSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path, include

from Apps.Account import views
urlpatterns = [
    path('get-account/', views.get_account),
    path('get-accounts/', views.get_accounts),
    path('index/', views.index),
    path('subjects/', views.subjects),
    path('getSubjectsold/', views.getSubjectsOld),
    path('addsubject/', views.addSubject),
    path('getFirstsubjects/', views.getFirstsubjects),
    path('getSecondSubjects/', views.getSecondSubjects),
    path('detailsubjects/', views.getDetailSubjects),
    path('getDetailSubjects/', views.getDetailSubjects),
    path('getCashSubjects/', views.getCashSubjects),
    path('upload/', views.upload),
    path('add_account/', views.add_account),
    path('get_addaccountdetailtabletdlist/', views.get_addaccountdetailtabletdlist),
    # 这以下是科目结构变更后添加的
    path('getSubjectType/', views.getSubjectType),  # 获取科目类别
    path('getSubjectCategory/', views.getSubjectCategory),  # 获取账户种类
    path('getSubjects/', views.getSubjects),
    path('getChildSubjects/', views.getChildSubjects),
    path('addAcount/', views.addAcount),
    path('getAccounts/', views.getAccounts),
    path('getAccountByParameter/', views.getAccountByParameter),
]
