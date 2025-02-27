from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from task_manager_app.models import Task, SubTask
from task_manager_app.serializer import TaskSerializer, CreateTaskSerializer, TaskDetailSerializer, SubTaskSerializer, \
    CreateSubTaskSerializer



class SubTaskListCreateView(APIView):
    def get(self, request):
        subtasks = SubTask.objects.all()
        serializer = SubTaskSerializer(subtasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        task = CreateSubTaskSerializer(data=request.data)
        if task:
            if task.is_valid():
                task.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)




class SubTaskDetailUpdateDeleteView(APIView):
    def get_subtask(self, pk):
        try:
            return SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return None

    def patch(self, request, pk):
        subtask = self.get_subtask(pk)
        if not subtask:
            return Response("{'error' 'Subtask not found'}",status=status.HTTP_404_NOT_FOUND)
        serializer = SubTaskSerializer(subtask, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request ,pk):
        subtask = self.get_subtask(pk)
        if not subtask:
            return Response("{'error' 'Subtask not found'}",status=status.HTTP_404_NOT_FOUND)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)







@api_view(['GET','POST'])
def get_task_list(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        task = CreateTaskSerializer(data=request.data)
        if task.is_valid():
            task.save()
            return Response(task.data, status=status.HTTP_201_CREATED)
        return Response(task.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_task_detail(request, pk):
    try:
        task = Task.objects.get(id=pk)
        task_detail = TaskDetailSerializer(task)
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
