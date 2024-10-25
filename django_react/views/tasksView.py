from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from SQLQueueCommunication.Models import Task
from SQLQueueCommunication.SqlServerConnection import SqlServerConnection
import json


@api_view(["GET", "POST"])
def tasksView(request):
    tasksFactory: SqlServerConnection = SqlServerConnection()
    if request.method == "POST":
        task_dict = request.data

        # Voorbeeld json:
        # {
        # "id": 14,
        # "task_type": "send_message",
        # "payload": {
        #     "hospital_id": "9610251011",
        #     "message": "testmessage"
        # },
        # "status": "completed",
        # "statuslog": "Hallo daar",
        # "retries": 5,
        # "priority": 5,
        # "created_at": "2024-10-22 12:58:49.820000",
        # "updated_at": "2024-10-24 11:37:23.120000",
        # "processed_at": "2024-10-24 11:37:22.933000",
        # "logTeller": 0
        # }

        new_task = Task(
        # id=task_dict["id"],
        task_type=task_dict["task_type"],
        payload=task_dict["payload"],
        status=task_dict["status"],
        # statuslog=task_dict["statuslog"],
        retries=task_dict["retries"],
        priority=task_dict["priority"],
        # created_at=datetime.strptime( task_dict["created_at"], '%Y-%m-%d %H:%M:%S.%f'),
        # updated_at=datetime.strptime( task_dict["updated_at"], '%Y-%m-%d %H:%M:%S.%f'),
        # processed_at=datetime.strptime( task_dict["processed_at"], '%Y-%m-%d %H:%M:%S.%f'),
        # logTeller=task_dict["logTeller"]
        )

        tasksFactory.insertTask(new_task)

        return Response({"message": "Succesvol toegvoegd!", "data": request.data})
    tasks_list = tasksFactory.getTasks()
    tasks_json = json.dumps([task.__dict__ for task in tasks_list], default=str)
    return Response(tasks_json)
