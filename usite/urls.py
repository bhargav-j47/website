from django.contrib import admin
from django.urls import path
from usite import views

urlpatterns = [
    path('',views.home,name='home'),
    path('contact',views.contact,name='contact'),
    path('login',views.login,name='login'),
    path('logout',views.logoutuser,name='logout'),
    path('signup',views.signup,name='signup'),
    path('blog',views.blog,name='blog'),
    path('blogs',views.blogpost,name='blogs'),
    path('search', views.search, name="search"),
] 