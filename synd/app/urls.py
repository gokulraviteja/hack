from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.admin_home),
    path('home',views.customer_home),
    path('login',views.login),
    path('register',views.register),
    path('customerDashboard',views.customer_dashboard),
    path('adminDashboard',views.admin_dashboard),
    path('logout',views.logout),
    path('pay',views.pay),
    path('receive',views.receive),
    path('profile',views.profile),
    path('money',views.money),
    path('transactions',views.transactions),
    path('result',views.result),
    path('groups',views.groups),
    path('groups/<str:grpname>/', views.display_group),
    path('addGroup',views.add_group),
    path('groups/<str:grpname>/addFriend', views.add_friend),
    path('groups/<str:grpname>/groupPay', views.group_pay),





]
