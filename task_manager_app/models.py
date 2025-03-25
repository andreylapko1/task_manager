from django.db import models
from django.utils import timezone

from task_manager_app.managers import SoftDeleteManager


class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In progress'),
        ('pending', 'Pending'),
        ('blocked', 'Blocked'),
        ('done', 'Done'),
    ]
    title = models.CharField(max_length=100)
    category = models.ForeignKey('Category', default=None, null=True, on_delete=models.SET_NULL)
    description = models.TextField(default=None)
    categories = models.ManyToManyField('Category', related_name='tasks', blank=True)
    status = models.CharField(max_length=100,choices=STATUS_CHOICES, default='new')
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SubTask(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In progress'),
        ('pending', 'Pending'),
        ('blocked', 'Blocked'),
        ('done', 'Done'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField(default=None)
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='subtasks')
    status =models.CharField(max_length=100, choices=STATUS_CHOICES, default='new')
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()




# Create your models here.
