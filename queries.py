import os
from django.utils import timezone
from datetime import timedelta
import django
from django.db.models import Q


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from task_manager_app.models import Task, SubTask

print(Task.objects.filter(status='new').values())
print(SubTask.objects.filter(Q(status='Done') & Q(deadline__lt=timezone.now())))

task = Task.objects.get(id=1)
task.status = 'In progress'
task.save()
print(Task.objects.filter(status='In progress').values())

subtask = SubTask.objects.get(id=1)
subtask.deadline = timezone.now() - timedelta(days=2)
subtask.save()

print(SubTask.objects.filter(id=1).values())

subtask2 = SubTask.objects.get(id=2)
subtask2.description = 'Create and format presentation slides'
subtask2.save()
print(SubTask.objects.filter(id=2).values())


del_task = Task.objects.get(id=1).delete()