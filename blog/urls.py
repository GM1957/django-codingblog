from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
   
    #api to post a comment
    path('postComment', views.postComment, name='postComment'),
    #path('', views.home, name='home'),
    path('<str:slug>', views.blogPost, name='blogPost'),
    path('', views.blogHome, name='blog'),
]
