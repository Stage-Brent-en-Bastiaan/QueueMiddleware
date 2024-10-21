from django.urls import path
from . import views

urlpatterns = [
    path('api/task/', views.TaskListCreate.as_view() ),
]