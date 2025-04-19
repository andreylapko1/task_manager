from django.utils import timezone
from rest_framework import serializers
from rest_framework.response import Response

from .models import Task, Category
from .models import SubTask

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'


class TaskDetailSerializer(serializers.ModelSerializer):
    # subtasks = SubTaskSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = '__all__'




class TaskDetailSubTaskStatusSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = '__all__'


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']



    def create(self, validated_data):
        if Category.objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError({"name": "Category already exists"})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data and validated_data['name'] != instance.name:
            if Category.objects.filter(name=validated_data['name']):
                raise serializers.ValidationError({"name": "Category already exists"})
            return super().update(instance, validated_data)


class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ('created_at ',)

class TaskSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = '__all__'

    def get_categories(self, obj):
        return [category.name for category in obj.categories.all()]


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'categories' ,'description', 'status', 'deadline',]

    def validate_deadline(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError({"deadline": "Deadline must be greater than now"})
        return value


class CreateSubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['title', 'task' ,'description', 'status', 'deadline']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


