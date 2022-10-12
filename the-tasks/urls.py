"""the-tasks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from tasksapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Sign up, Login and Logout
    path('signup/', views.sign_up_user, name='sign_up_user'),
    path('login/', views.log_in_user, name='log_in_user'),
    path('logout/', views.log_out_user, name='log_out_user'),

    # Tasks
    path('', views.home, name='home'),
    path('create/', views.create_task, name='create_task'),
    path('current/', views.current_tasks, name='current_tasks'),
    path('completed/', views.completed_tasks, name='completed_tasks'),
    path('task/<int:task_pk>', views.task_page, name='task_page'),
    path('task/<int:task_pk>/complete/', views.complete_task, name='complete_task'),
    path('task/<int:task_pk>/delete/', views.delete_task, name='delete_task'),
    path('task/<int:task_pk>/redo/', views.redo_task, name='redo_task'),
]