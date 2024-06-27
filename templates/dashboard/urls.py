# dashboard/urls.py

from django.urls import path
from . import views
from templates.tasks.views import (task_list,
                                   create_task,
                                   update_task,
                                   delete_task
                                   )

urlpatterns = [
    path('dashboard', views.index, name='dashboard'),
    path('tasks', task_list, name='tasks'),
    path('create/', create_task, name='create_task'),
    path('tasks/update/<int:pk>/', update_task, name='update_task'),
    path('tasks/delete/<int:pk>/', delete_task, name='delete_task'),
]
