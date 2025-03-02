from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from task_manager_app.models import Task, SubTask
from task_manager_app.serializer import TaskSerializer, CreateTaskSerializer, TaskDetailSerializer, SubTaskSerializer, \
    CreateSubTaskSerializer, TaskDetailSubTaskStatusSerializer
from rest_framework.pagination import PageNumberPagination



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






class TaskListCreateView(APIView, PageNumberPagination):

    page_size = 5
    def get_page_size(self, request):
        page_size = request.query_params.get('page_size')
        if page_size and page_size.isdigit():
            return int(page_size)
        return self.page_size



    def get_task_name(self, request):
        task_name = request.query_params.get('task_name')
        if task_name:
            return task_name
        return None

    def get_subtask_status(self, request):
        subtask_status = request.query_params.get('subtask_status')
        if subtask_status:
            return subtask_status
        return None

    def get_week_day(self, request):
        week_day = request.query_params.get('week_day')
        if week_day and week_day.isdigit():
            return int(week_day)
        return None


    def get(self, request):
        week_day = self.get_week_day(request)
        task_name = self.get_task_name(request)
        subtask_status = self.get_subtask_status(request)

        tasks = Task.objects.all().order_by('-created_at')

        if week_day:
            tasks = tasks.filter(created_at__week_day=week_day).order_by('-created_at')

        if task_name:
            tasks = tasks.filter(title__icontains=task_name)

        if subtask_status:
            tasks = tasks.filter(subtasks__status=subtask_status)

        page_size = self.get_page_size(request)
        results = self.paginate_queryset(tasks, request, view=self)
        if subtask_status:
            serializer = TaskDetailSubTaskStatusSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = TaskDetailSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


    def post(self, request):
        serializer = CreateTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailCreateUpdateDeleteView(APIView):

    def get_task(self, pk):
        try:
            task = Task.objects.get(pk=pk)
            return task
        except Task.DoesNotExist:
            return None

    def get(self, request, pk):
        task = self.get_task(pk)

        if task is None:
            return Response({'error': 'Task not found'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = self.get_task(pk)
        if task is None:
            return Response({'error': 'Task not found'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TaskDetailSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskCountView(APIView):

    def get(self, request, stat=None):
        if stat is None:
            tasks = Task.objects.all().count()
            return Response({'Count tasks': tasks}, status=status.HTTP_200_OK)
        if stat:
            valid_statuses = ['new', 'in_progress', 'pending', 'blocked', 'done']
            if stat not in valid_statuses:
                return Response({'message': 'Status not supported'})
            tasks = Task.objects.filter(status=stat)
            if not tasks:
                return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)

class TaskOverdueCountView(APIView):
    def get(self, request):
        count = 0
        overdue_task_list = []
        overdue_tasks = Task.objects.all()
        for task in overdue_tasks:
            if task.deadline < timezone.now():
                overdue_task_list.append(task.title)
                count += 1
        return Response({'Count overdue task': count, 'Overdue tasks': f'{overdue_task_list}'}, status=status.HTTP_200_OK)




# Create your views here.
