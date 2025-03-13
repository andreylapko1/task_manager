from django.contrib import admin
from django.utils.timezone import override

from .models import Task, SubTask, Category



class SubTaskInline(admin.StackedInline):
    model = SubTask
    extra = 1
    classes = ['collapse']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [SubTaskInline]
    list_display = ('title_short', 'description', 'status', 'deadline')
    list_filter = ('status', 'deadline')

    def title_short(self, obj):
        return obj.title[:10] + '...' if len(obj.title) > 10 else obj.title


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title','description', 'status', 'deadline')
    actions = ['to_done', 'in_progress']


    @admin.action(description='Done')
    def to_done(self, request, obj):
        obj.update(status='done')

    @admin.action(description='In progress')
    def in_progress(self, request, obj):
        obj.update(status='in_progress')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass



# Register your models here.
