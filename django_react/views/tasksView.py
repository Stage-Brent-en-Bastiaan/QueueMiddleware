from rest_framework.decorators import api_view
from rest_framework.response import Response
from SQLQueueCommunication.SqlServerConnection import SqlServerConnection
import json

@api_view(['GET'])
def tasksView(request):
    tasksFactory: SqlServerConnection = SqlServerConnection()

    tasks_list = tasksFactory.getTasks()

    tasks_json = json.dumps([task.__dict__ for task in tasks_list])

    return Response(tasks_json)