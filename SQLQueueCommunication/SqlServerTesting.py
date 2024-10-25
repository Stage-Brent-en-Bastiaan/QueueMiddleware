import json
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

    def createDummyTask(self) -> Task:
        fake = Faker()  # Initialize Faker
        hospitalIdsToUse = ["9610251011", "9203161015","1"]

        # Generate a random ID for the task
        task_id = random.randint(1, 100)  # Example range; adjust as necessary
        hospital_id = random.choice(hospitalIdsToUse)
        created_at = fake.date_time_this_month()
        status = random.choice(self.statuses)
        retries = 0
        updated_at = None
        processed_at = None
        if status == "in_queue":
            retries = 0
        else:
            updated_at = fake.date_time_between(datetime.now(), created_at)
            processed_at = updated_at
            retries = random.randint(1, 4)
        # Create a dummy task instance
        dummy_task = Task(
            id=task_id,
            task_type="send_message",
            payload={"hospital_id": hospital_id.__str__(), "message": fake.sentence()},
            status=status,
            statuslog="created",
            retries=retries,
            priority=random.randint(1, 10),
            created_at=created_at,
            updated_at=updated_at,
            processed_at=processed_at,
            logTeller=random.randint(1, 10),
        )
        return dummy_task
