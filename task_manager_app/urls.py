from django.urls import path, include
from . import views

urlpatterns = [
    path('task_create/', views.task_create, name='task_create'),
]