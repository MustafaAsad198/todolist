from django.contrib import admin
from django.urls import path,include
from .views import Taskdetail, Tasklist,Taskcreate,Taskupdate,Taskdelete,Customloginview,Register
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',Tasklist.as_view(),name='tasks'),
    path('task/<int:pk>/',Taskdetail.as_view(),name='task'),
    path('task-create/',Taskcreate.as_view(),name='task-create'),
    path('task-update/<int:pk>/',Taskupdate.as_view(),name='task-update'),
    path('task-delete/<int:pk>/',Taskdelete.as_view(),name='task-delete'),
    path('login/',Customloginview.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('register/',Register.as_view(),name='register'),
    
]