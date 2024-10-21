from django.db import models

class Task(models.Model):
    task_type = models.CharField(max_length=25)
    payload = models.TextField()
    status = models.CharField(max_length=20)
    statuslog = models.CharField(max_length=255)
    retries = models.IntegerField()
    priority = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)


