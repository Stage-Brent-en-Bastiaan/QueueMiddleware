from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'task_type', 'payload', 'status', 'statuslog', 'retries', 'priority', 'created_at', 'updated_at', 'processed_at')