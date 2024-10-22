from .models import Task
from .serializers import TaskSerializer
from rest_framework import generics

class TaskListCreate(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
