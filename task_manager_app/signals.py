from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from task_manager_app.models import Task


@receiver(pre_save, sender=Task)
def task_complete_or_status_change(sender, instance, *args, **kwargs):
    if instance.pk:
        old_instance = Task.objects.get(pk=instance.pk)
        pre_status = old_instance.status
        post_status = instance.status
        if pre_status != post_status:
            print(f'Status {instance.title} change from {pre_status} to {post_status} ')
