from django.urls import path, include
from . import views

urlpatterns = [

    path('task_detail/<int:pk>', views.TaskDetailCreateUpdateDeleteView.as_view(), name='task_list'),
    path('task_list/', views.TaskListCreateView.as_view(), name='task_list'),
    path('create_subtask/', views.SubTaskListCreateView.as_view(), name='create_subtask'),
    path('update_subtask/<int:pk>', views.SubTaskDetailUpdateDeleteView.as_view(), name='update_delete_subtask'),
    path('task_count/', views.TaskCountView.as_view(), name='get_task_count'),
    path('status/<str:stat>', views.TaskCountView.as_view(), name='count_task_by_status'),
    path('overdue_task/', views.TaskOverdueCountView.as_view(), name='count_overdue_tasks'),
]