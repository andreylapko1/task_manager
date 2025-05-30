from django.db.models import Count
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy
from rest_framework.views import APIView

from task_manager_app.forms import UserRegisterForm
from task_manager_app.models import Task, SubTask, Category
from task_manager_app.serializer import TaskSerializer, CreateTaskSerializer, TaskDetailSerializer, SubTaskSerializer, \
    CategoryCreateSerializer, UserRegistrationSerializer
from rest_framework.pagination import PageNumberPagination



class SubTaskListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer


class TaskListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAdminUser]
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer


class TaskCountView(APIView):
    permission_classes = [IsAdminUser]

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
    permission_classes = [IsAdminUser]
    def get(self, request):
        count = 0
        overdue_task_list = []
        overdue_tasks = Task.objects.all()
        for task in overdue_tasks:
            if task.deadline < timezone.now():
                overdue_task_list.append(task.title)
                count += 1
        return Response({'Count overdue task': count, 'Overdue tasks': f'{overdue_task_list}'}, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer

    @action(detail=False, methods=['GET'])
    def count_tasks(self, request):
        categories = Category.objects.annotate(tasks_count=Count('tasks'))
        response = []
        for category in categories:
            response.append({
                'id': category.pk,
                'title': category.name,
                'tasks_count': category.tasks_count
            })
        return Response(response)


class UserRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'username': user.username, 'email': user.email}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
