from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from task_manager_app.serializer import TaskSerializer



@api_view(['POST'])
def task_create(request):
    task = TaskSerializer(data=request.data)
    if task.is_valid():
        task.save()
        return Response(task.data, status=status.HTTP_201_CREATED)
    return Response(task.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
