# from django.test import TestCase
import json
from ApiCommunication.Patienten import Patienten
from SQLQueueCommunication.SqlServerTesting import SqlServerTesting
from SQLQueueCommunication.SqlServerConnection import SqlServerConnection
# Create your tests here.
conn=SqlServerTesting()
print(conn.insertTask())
