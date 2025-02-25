from rest_framework import serializers
from .models import Task
from .models import SubTask


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']