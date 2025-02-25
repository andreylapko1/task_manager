from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from task_manager_app.models import Task
from task_manager_app.serializer import TaskSerializer, CreateTaskSerializer



@api_view(['POST'])
def task_create(request):
    task = CreateTaskSerializer(data=request.data)
    if task.is_valid():
        task.save()
        return Response(task.data, status=status.HTTP_201_CREATED)
    return Response(task.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_task_list(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_task_detail(request, pk):
    try:
        task = Task.objects.get(id=pk)
        task_detail = TaskSerializer(task)
        return Response(task_detail.data)
    except Task.DoesNotExist:
        return Response({'message': 'Not Found'},status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_task_count(request):
    tasks = Task.objects.all().count()
    return Response({'Count tasks': tasks}, status=status.HTTP_200_OK)

@api_view(['GET'])
def count_task_by_status(request, status):
    valid_statuses = ['new', 'in_progress', 'pending', 'blocked', 'done']
    if status not in valid_statuses:
        return Response({'message': 'Status not supported'})
    tasks = Task.objects.filter(status=status)
    if not tasks:
        return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def count_overdue_tasks(request):
    count = 0
    overdue_task_list = []
    overdue_tasks = Task.objects.all()
    for task in overdue_tasks:
        if task.deadline < timezone.now():
            overdue_task_list.append(task.title)
            count += 1
    return Response({'Count overdue task': count, 'Overdue tasks': f'{overdue_task_list}'}, status=status.HTTP_200_OK)


# Create your views here.
