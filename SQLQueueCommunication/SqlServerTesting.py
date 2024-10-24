from .SqlServerConnection import SqlServerConnection
from .Models import *
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from faker import Faker
import random
class SqlServerTesting(SqlServerConnection):
    def __init__(self) -> None:
        super().__init__()
    def insertTask(self,newTask:Task):
        query = """
        INSERT INTO Tasks (
            task_type, payload, status, statuslog, retries,
            priority, created_at, updated_at, processed_at, logTeller
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        values = (
            newTask.task_type,
            newTask.payload,
            newTask.status,
            newTask.statuslog,
            newTask.retries,
            newTask.priority,
            newTask.created_at,
            newTask.updated_at,
            newTask.processed_at,
            newTask.logTeller
        )
        cursor=self.connection.cursor()
        cursor.execute(query,values)
        cursor.commit()
    def createDummyTask(self)->Task:
        fake = Faker()  # Initialize Faker
        hospitalIdsToUse=["9610251011","9203161015"]
        
        # Generate a random ID for the task
        task_id = random.randint(1,100)  # Example range; adjust as necessary
        hospital_id=hospitalIdsToUse[random.randint(1,hospitalIdsToUse.__len__()-1)]
        created_at=fake.date_time_this_month
        # Create a dummy task instance
        dummy_task = Task(
          id=task_id,
          task_type=fake.word(),  # Random word for task type
          payload={"hospital_id": hospital_id, "message": "testmessage"},  # Random sentence for payload
          status=random.choice(self.statuses),  # Random status
          statuslog=fake.text(),  # Random text for status log
          retries=random.randint(0, 5),  # Random retries between 0 and 5
          priority=random.randint(1, 10),  # Random priority between 1 and 10
          created_at=created_at,
          updated_at=datetime.now(),
          processed_at=fake.date_time_this_month,
          logTeller=random.randint(1, 10)  # Random log teller
        )
        return dummy_task

        