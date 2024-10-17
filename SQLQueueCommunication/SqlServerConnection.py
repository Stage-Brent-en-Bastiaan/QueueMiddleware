import configparser
import pyodbc
from .Models import *

class SqlServerConnection:
    def __init__(self)-> None:
        #get needed config data from ini file and create a new connection 
        config = configparser.ConfigParser()
        config.read(".ini")
        dbconfiguration=config["queue_db"]
        server = dbconfiguration["server"]
        database = dbconfiguration["database"]
        username = dbconfiguration["username"]
        password = dbconfiguration["password"]
        connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        connection = pyodbc.connect(connection_string)
        self.connection=connection

    def getFirstQueueItem(self) -> Task:
        statusToUse="pending"
        query="""SELECT Top 1 id, task_type, payload, status, statuslog, retries, priority, created_at, updated_at, processed_at 
            FROM tasks_queue
            WHERE Status = ?"""
        cursor = self.connection.cursor()
        cursor.execute(query,statusToUse)
        tasks = []
        for row in cursor.fetchall():
            task = Task(
                id=row.id,
                task_type=row.task_type,
                payload=row.payload,  # Assuming payload is a JSON string or dict
                status=row.status,
                statuslog=row.statuslog,
                retries=row.retries,
                priority=row.priority,
                created_at=row.created_at,
                updated_at=row.updated_at,
                processed_at=row.processed_at
            )
            tasks.append(task)
        cursor.close()
        if(tasks.__len__()<=0):
            return None
        else:
            return tasks[0]