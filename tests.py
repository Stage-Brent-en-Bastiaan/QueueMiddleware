# from django.test import TestCase
import json
from ApiCommunication.Patienten import Patienten
from SQLQueueCommunication.SqlServerConnection import SqlServerConnection
# Create your tests here.
conn=SqlServerConnection()
print(conn.getTasks())
