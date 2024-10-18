import time
from SQLQueueCommunication.SqlServerConnection import *
from SQLQueueCommunication.Models import *
from .ApiCommunication.Messages import *
from .ApiCommunication.Patienten import *
class QueueManager:
    

    def __init__(self) -> None:
        self.taskDict:dict[str,function]={'send_message':self.sendMessage,'test_task':self.testTask}
    def main(self):
        running=True
        while(running):
            serverConnection=SqlServerConnection()

            # Fetch data
            firstQueueTask = serverConnection.getFirstPendingQueueItem()

            if (firstQueueTask==None):
                pass
            else:
                self.handleTask(firstQueueTask)
            #wacht 5 seconden
            time.sleep(1)
            running=False
    def handleTask(self,task:Task)->None:
        taskType:TaskType=task.task_type
        task.processed_at=datetime()
        task.update_status(self.taskDict.get(task.task_type)(task.payload))
    def sendMessage(self,payload:Any)->str:
        pass
    def testTask(self,payload:Any)->str:
        pass
        
            