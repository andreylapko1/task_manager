from django.urls import path, include
from . import views

urlpatterns = [

    path('task_detail/<int:pk>', views.TaskDetailCreateUpdateDeleteView.as_view(), name='task_list'),
    path('task_list/', views.TaskListCreateView.as_view(), name='task_list'),
    path('create_subtask/', views.SubTaskListCreateView.as_view(), name='create_subtask'),
    path('update_subtask/<int:pk>', views.SubTaskDetailUpdateDeleteView.as_view(), name='update_delete_subtask'),
    path('task_count/', views.get_task_count, name='get_task_count'),
    path('status/<str:status>', views.count_task_by_status, name='count_task_by_status'),
    path('overdue_task/', views.count_overdue_tasks, name='count_overdue_tasks'),
]