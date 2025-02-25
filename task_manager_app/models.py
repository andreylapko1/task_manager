from django.db import models


class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In progress'),
        ('pending', 'Pending'),
        ('blocked', 'Blocked'),
        ('done', 'Done'),
    ]
    title = models.CharField(max_length=100)
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
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    status =models.CharField(max_length=100, choices=STATUS_CHOICES, default='new')
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



# Create your models here.
