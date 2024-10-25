# from django.test import TestCase
import json
from BewellApiCommunication.Patienten import Patienten
from SQLQueueCommunication.SqlServerTesting import SqlServerTesting

class Testing:
    def main(self):
        print(self.printAllData())
    #add 30 random tasks in the database queue
    def insertDummyTasks(self):
        conn = SqlServerTesting()
        for x in range(10):
            task = conn.createDummyTask()
            print("-nieuwe task te inserten")
            conn.insertTask(task)
            print("inserted")
        print("-finished")
    def printAllData(self):
        conn = SqlServerTesting()
        print(conn.getTasks())

testing=Testing()
testing.main()


