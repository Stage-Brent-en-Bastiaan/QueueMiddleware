from rest_framework import serializers

from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'task_type', 'payload', 'status', 'statuslog', 'retries', 'priority', 'created_at', 'updated_at', 'processed_at')
class PatientSerializer(serializers.Serializer):
     id = serializers.IntegerField()
     address = serializers.CharField()
     box_code = serializers.CharField()
     date_of_birth = serializers.DateField()
     first_name = serializers.CharField()
     gender = serializers.CharField()
     gov_id = serializers.CharField()
     hospital_id = serializers.CharField()
     last_name = serializers.CharField()
     locale = serializers.CharField()
     nationality = serializers.CharField()
     phone_contact = serializers.CharField()

     def read (self, instance):
         return {
        "address": null,
        "box_code": "mxjc1xe987irze64",
        "date_of_birth": "1986-08-08",
        "first_name": "Bob",
        "gender": "male",
        "gov_id": "11320079431",
        "hospital_id": null,
        "id": 394,
        "last_name": "Marly",
        "locale": null,
        "nationality": null,
        "phone_contact": null
    }