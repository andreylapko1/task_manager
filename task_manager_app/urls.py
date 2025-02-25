from django.urls import path, include
from . import views

urlpatterns = [
    path('task_create/', views.task_create, name='task_create'),
    path('task_list/', views.get_task_list, name='task_list'),
    path('task_detail/<int:pk>', views.get_task_detail, name='task_detail'),
    path('task_count/', views.get_task_count, name='get_task_count'),
    path('status/<str:status>', views.count_task_by_status, name='count_task_by_status'),
    path('overdue_task/', views.count_overdue_tasks, name='count_overdue_tasks'),
]