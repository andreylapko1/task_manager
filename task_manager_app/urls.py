from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import CategoryUpdateView



urlpatterns = [

    path('task_detail/<int:pk>', views.TaskDetailCreateUpdateDeleteView.as_view(), name='task_list'),
    path('task_list/', views.TaskListCreateView.as_view(), name='task_list'),
    path('create_subtask/', views.SubTaskListCreateView.as_view(), name='create_subtask'),
    path('update_subtask/<int:pk>', views.SubTaskDetailUpdateDeleteView.as_view(), name='update_delete_subtask'),
    path('task_count/', views.TaskCountView.as_view(), name='get_task_count'),
    path('status/<str:stat>', views.TaskCountView.as_view(), name='count_task_by_status'),
    path('overdue_task/', views.TaskOverdueCountView.as_view(), name='count_overdue_tasks'),
    path('category/', views.CategoryViewSet.as_view({'get': 'list'}), name='category_list'),
    path('category/<int:pk>', views.CategoryUpdateView.as_view({'put': 'update', 'get': 'retrieve', 'delete': 'destroy',
                                                                # 'action': 'count_tasks_by_category'
                                                                }), name='category_list'),
    path('category/<int:pk>/count_tasks', views.CategoryUpdateView.as_view({'get': 'count_tasks_by_category',}), name='count_category_tasks'),
]
