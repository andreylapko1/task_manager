from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserRegistrationViewSet

router = DefaultRouter()
router.register('category', views.CategoryViewSet)


urlpatterns = [

    path('task_detail/<int:pk>', views.TaskDetailCreateUpdateDeleteView.as_view(), name='task_list'),
    path('task_list/', views.TaskListCreateView.as_view(), name='task_list'),
    path('create_subtask/', views.SubTaskListCreateView.as_view(), name='create_subtask'),
    path('update_subtask/<int:pk>', views.SubTaskDetailUpdateDeleteView.as_view(), name='update_delete_subtask'),
    path('task_count/', views.TaskCountView.as_view(), name='get_task_count'),
    path('status/<str:stat>', views.TaskCountView.as_view(), name='count_task_by_status'),
    path('overdue_task/', views.TaskOverdueCountView.as_view(), name='count_overdue_tasks'),
    path('', include(router.urls), name='count_task'),
    path('token-obtain/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationViewSet.as_view({'post': 'create'}), name='register'),
]