import configparser
import pyodbc
from .Models import *
import json
from Settings import Settings


class SqlServerConnection:
    def __init__(self) -> None:
        # get needed config data from ini file and create a new connection
        config = configparser.ConfigParser()
        config.read(".ini")
        dbconfiguration = config["queue_db"]
        server = dbconfiguration["server"]
        database = dbconfiguration["database"]
        username = dbconfiguration["username"]
        password = dbconfiguration["password"]
        connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        connection = pyodbc.connect(connection_string)
        # store connection in a variable
        self.connection: pyodbc.Connection = connection
        settingsfactory = Settings()
        self.statuses: dict[str:str] = settingsfactory.statuses
        self.maxPriority = settingsfactory.maxPriority

        # self.delaydict:dict[int,int]={0:0,1:60,2:120,3:240}

    def getNextQueueItem(self) -> Task:
        response = None
        response = self.getFirstQueItem()
        return response

    # geef de eerste queueitem(task) met de hoogste prioriteit en de laagste aantal retries en minder dan settings.maxretries
    def getFirstQueItem(self) -> Task:
        query = """
        SELECT top 1 q.ID, q.task_type, q.payload, q.status, q.statuslog, q.retries, q.priority, q.created_at, q.updated_at, q.processed_at
        FROM dbo.tasks_queue AS q LEFT OUTER JOIN
             dbo.task_type AS tt ON q.task_type = tt.task_type
        WHERE status IN (?, ?) 
              AND DATEDIFF(MINUTE, updated_at, GETDATE()) > (tt.retryinterval*(2^q.retries))-1 
              And q.retries<tt.maxretries
        ORDER BY q.priority, q.ID
        """
        values = (self.statuses["in_queue"], self.statuses["failed"])
        # print("-executing: ",query, " -with values: ",values)
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        tasks = []
        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            # print("payload", row.payload)
            firstTask = Task(
                id=row.ID,
                task_type=row.task_type,
                payload=json.loads(row.payload),
                status=row.status,
                statuslog=row.statuslog,
                retries=row.retries,
                priority=row.priority,
                created_at=row.created_at,
                updated_at=row.updated_at,
                processed_at=row.processed_at,
            )
            tasks.append(firstTask)
        if tasks.__len__() == 0:
            return None
        else:
            if tasks.__len__() > 1:
                raise ValueError("er werden meerdere tasks gevonden")
            firstTask: Task = tasks[0]
            return firstTask

    # deprecated
    def getFirstPendingQueueItem(self) -> Task:
        statusToUse: str = self.statuses[0]
        query = """
            SELECT Top 1 id, task_type, payload, status, statuslog, retries, priority, created_at, updated_at, processed_at 
            FROM tasks_queue
            WHERE Status = ?
            """
        cursor = self.connection.cursor()
        cursor.execute(query, statusToUse)
        tasks = []
        for row in cursor.fetchall():
            # print("payload", row.payload)
            firstTask = Task(
                id=row.id,
                task_type=row.task_type,
                payload=json.loads(
                    row.payload
                ),  # Assuming payload is a JSON string or dict
                status=row.status,
                statuslog=row.statuslog,
                retries=row.retries,
                priority=row.priority,
                created_at=row.created_at,
                updated_at=row.updated_at,
                processed_at=row.processed_at,
            )
            tasks.append(firstTask)
        cursor.close()
        if tasks.__len__() == 0:
            print("-no new tasks found")
            return None
        else:
            if tasks.__len__() > 1:
                print(
                    "--Fout: er is meer dan 1 task gevonden maar er werd er maar 1 verwacht"
                )
                raise ValueError("er werden meerdere tasks gevonden")
            firstTask: Task = tasks[0]
            print("-task(s) found:", tasks.__len__())
            return firstTask

    def updateTask(self, task: Task) -> None:
        query = """
            UPDATE tasks_queue
            SET 
                status = ?, 
                statuslog = ?, 
                retries = ?, 
                created_at = ?, 
                updated_at = ?, 
                processed_at = ?
            WHERE ID = ?
            """
        # Values to update in the database (use the task values)
        values = (
            task.status,
            task.statuslog,
            task.retries,
            task.created_at,
            task.updated_at,
            task.processed_at,
            task.id,
        )
        cursor = self.connection.cursor()
        # print("-updating with values:",values)
        cursor.execute(query, values)
        cursor.commit()
        cursor.close()

    def getTasks(self) -> list[Task]:
        query = """
            SELECT id, task_type, payload, status, statuslog, retries, priority, created_at, updated_at, processed_at 
            FROM tasks_queue
            """
        cursor = self.connection.cursor()
        cursor.execute(query)
        tasks = []
        for row in cursor.fetchall():
            # print("payload", row.payload)
            firstTask = Task(
                id=row.id,
                task_type=row.task_type,
                payload=json.loads(
                    row.payload
                ),  # Assuming payload is a JSON string or dict
                status=row.status,
                statuslog=row.statuslog,
                retries=row.retries,
                priority=row.priority,
                created_at=row.created_at,
                updated_at=row.updated_at,
                processed_at=row.processed_at,
            )
            tasks.append(firstTask)
        cursor.close()
        return tasks

    def insertTask(self, newTask: Task):
        query = """
        INSERT INTO tasks_queue (
            task_type, payload, status, statuslog, retries,
            priority, created_at, updated_at, processed_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        payload = json.dumps(newTask.payload)
        values = (
            newTask.task_type,
            payload,
            newTask.status,
            newTask.statuslog,
            newTask.retries,
            newTask.priority,
            newTask.created_at,
            newTask.updated_at,
            newTask.processed_at,
        )
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        cursor.commit()
