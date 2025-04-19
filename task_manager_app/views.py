from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, UpdateAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from task_manager_app.models import Task, SubTask, Category
from task_manager_app.serializer import TaskSerializer, CreateTaskSerializer, TaskDetailSerializer, SubTaskSerializer, \
    CategorySerializer, CategoryCreateUpdateSerializer
from rest_framework.pagination import PageNumberPagination



class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]

    filterset_fields = [
        'status','deadline',
    ]
    search_fields = [
        'title', 'description',
    ]

    ordering_fields = [
        'created_at',
    ]



class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer


class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    pagination_class = PageNumberPagination
    page_size = 5

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ['title',
                        'description',]

    search_fields = ['status', 'deadline']

    ordering_fields =  ['created_at']



    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTaskSerializer
        elif self.request.method == 'GET':
            return TaskSerializer

    def get_page_size(self, request):
        page_size = request.query_params.get('page_size')
        if page_size and page_size.isdigit():
            return int(page_size)
        return self.page_size

    def get_queryset(self):
        page_size = self.get_page_size(self.request)
        self.pagination_class.page_size = page_size
        task_name = self.request.query_params.get('task_name')
        subtask_status = self.request.query_params.get('subtask_status')
        week_day = self.request.query_params.get('week_day')
        queryset = super().get_queryset()
        if task_name:
            queryset = queryset.filter(title__icontains=task_name)
        if subtask_status:
            queryset = queryset.filter(subtasks__status=subtask_status)
        if week_day:
            queryset = queryset.filter(created_at__week_day=week_day).order_by('-created_at')
        return queryset.order_by('pk')






class TaskDetailCreateUpdateDeleteView(RetrieveUpdateDestroyAPIView ):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer


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



class CategoryViewSet(ModelViewSet, CreateAPIView):
    serializer_class = CategorySerializer


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategoryCreateUpdateSerializer
        if self.request.method == 'GET':
            return CategorySerializer


    def get_queryset(self):
        return Category.objects.filter(is_deleted=False)




class CategoryUpdateView(viewsets.ModelViewSet):
    serializer_class = CategoryCreateUpdateSerializer

    def get_queryset(self,  *args, **kwargs):
        pk = self.kwargs.get('pk')
        return Category.objects.filter(pk=pk)

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        category.is_deleted = True
        category.deleted_at = timezone.now()
        category.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get']) # Кнопки нет, но url работает
    def count_tasks_by_category(self, request, pk):
        category = self.get_object()
        count = Task.objects.filter(categories=category).count()
        return Response({'count': count})




# Create your views here.
