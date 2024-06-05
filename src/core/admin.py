from django.contrib import admin
from core.models import Todo


class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'priority', 'complete_before',
                    'to_be_notified', 'is_notified', 'is_completed', 'user',
                    'created_at']


#  Register model to the admin site.
admin.site.register(Todo, TodoAdmin)
