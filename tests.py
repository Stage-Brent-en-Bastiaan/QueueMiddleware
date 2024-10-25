# from django.test import TestCase
import json
from ApiCommunication.Patienten import Patienten
from SQLQueueCommunication.SqlServerTesting import SqlServerTesting
# Create your tests here.
conn=SqlServerTesting()
for x in range(30):
    task=conn.createDummyTask()
    print("-nieuwe task te inserten")
    conn.insertTask(task)
    print("inserted")
print("-finished")
