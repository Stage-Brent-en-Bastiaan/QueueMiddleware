# from django.test import TestCase
import json
from BewellApiCommunication.Patienten import Patienten
from SQLQueueCommunication.SqlServerTesting import SqlServerTesting
from QueueManager import QueueManager


class Testing:
    def main(self):
        self.insertDummyTasks(20)

    # add 30 random tasks in the database queue
    def insertDummyTasks(self, aantal: int):
        conn = SqlServerTesting()
        for x in range(aantal):
            task = conn.createDummyTask()
            print("-nieuwe task te inserten")
            conn.insertTask(task)
            print("inserted")
        print("-finished")

    def printAllData(self):
        conn = SqlServerTesting()
        print(conn.getTasks())


testing = Testing()
testing.main()
# QueueManager = QueueManager()
# QueueManager.main()
