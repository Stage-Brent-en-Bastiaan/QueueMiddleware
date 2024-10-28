from rest_framework.decorators import api_view
from rest_framework.response import Response
from QueueManager import QueueManager
import json


@api_view()
def ExecuteTasks(request):
    queueManager = QueueManager()
    queueManager.action()

    return Response("")
