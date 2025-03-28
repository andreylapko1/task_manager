from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
# from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from rest_framework.response import Response
from rest_framework.validators import UniqueValidator

from .models import Task, Category
from .models import SubTask

class SubTaskSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    class Meta:
        model = SubTask
        fields = '__all__'


class TaskDetailSerializer(serializers.ModelSerializer):
    # subtasks = SubTaskSerializer(many=True, read_only=True)
    owner = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    class Meta:
        model = Task
        fields = '__all__'




class TaskDetailSubTaskStatusSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = '__all__'


class CategoryCreateSerializer(serializers.ModelSerializer):
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
    owner = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    class Meta:
        model = Task
        fields = '__all__'


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline', ]

    def validate_deadline(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError({"deadline": "Deadline must be greater than now"})
        return value


class CreateSubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['title', 'task' ,'description', 'status', 'deadline']



class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    password_repeat = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['username', 'password','password_repeat', 'email']

    def validate(self, data):
        if data['password'] != data['password_repeat']:
            raise serializers.ValidationError({"repeat_password": "Passwords do not match"})
        data.pop('password_repeat')
        return data

    def validate_username(self, value):
        if not value.isalnum():
            raise serializers.ValidationError({"username": "Username must be alphanumeric"})
        return value










