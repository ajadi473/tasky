# dashboard/urls.py

from django.urls import path
from . import views
from templates.tasks.views import (task_list,
                                   create_task,
                                   update_task,
                                   delete_task,
                                   task_detail,
                                   move_task
                                   )

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('tasks', task_list, name='tasks'),
    path('create/', create_task, name='create_task'),
    path('tasks/update/<int:pk>/', update_task, name='update_task'),
    path('tasks/delete/<int:pk>/', delete_task, name='delete_task'),
    path('tasks/<int:pk>/detail/', task_detail, name='task_detail'),
    path('move-tasks/<int:pk>/', move_task, name='move_task'),
    path('search/', views.search_tasks, name='search_tasks'),
]
