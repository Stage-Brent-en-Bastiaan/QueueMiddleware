import time
from SQLQueueCommunication.SqlServerConnection import *
from SQLQueueCommunication.Models import *
from ApiCommunication.Messages import Messages
from ApiCommunication.Patienten import Patienten
from ApiCommunication.Models2 import *
from Settings import Settings


class QueueManager:
    def __init__(self) -> None:
        # dit zijn alle types van tasks de kunnen uitgevoerd worden: ze worden gelinkt aan een methode
        settings = Settings()
        self.taskDict: dict[str, function] = {
            "send_message": self.sendMessage,
            "test_task": self.testTask,
        }
        self.statuses = list(settings.statuses)
        self.delay = settings.maindelay

    # het programmaverloop
    def main(self):
        teller = 0
        amountofloops = 2
        running = True
        # program loop
        while running:
            serverConnection = SqlServerConnection()

            # Fetch data
            firstQueueTask = serverConnection.getFirstPendingQueueItem()

            if firstQueueTask == None:
                pass
            else:
                self.handleTask(firstQueueTask)
            # wacht
            time.sleep(self.delay)
            if teller >= amountofloops - 1:
                running = False
                print("ending queueprogram loop")
            teller = teller + 1

    # behandeld de doorgestuurde task
    def handleTask(self, task: Task) -> None:
        task.start_process()
        conn = SqlServerConnection()
        conn.updateTask(task)
        # get the function from taskdict that is linked to the task type name and execute it,
        statusReturned: list[str] = self.taskDict.get(task.task_type)(task.payload)
        # return the returned status to the update_status method
        task.update_status(statusReturned)
        conn.updateTask(task)

    # taskdict methods, should all look the same
    def sendMessage(self, payload) -> list[str]:
        log=""
        print("-executing send message task, payload:", payload)
        #check wether payload is the correct type
        if not isinstance(payload, dict):
            return (
                self.statuses[3],
                """geef een juiste payload terug de payload voor sendmessage moet er zo uitzien { "patient_number":"7402241006","message":"Graag je huisarts contacteren voor meer info"}""",
            )
        payload: dict[str, str] = payload

        #get the patient from the bewell api
        patientenFactory = Patienten()
        hospitalId=payload["hospital_id"]
        print("searching for patient met hospital_id: ", hospitalId)
        patient = patientenFactory.getPatientHospitalId(hospitalId)
        if patient == None:
            return [self.statuses[3], "deze patient bestaat niet in de bewell omgeving"]
        else:
            print("patient gevonden: ", patient)
            log=log+"patient is gevonden, "
            #todo: verstuur message naar de gevonden patient
            newMessage=MessagePost(recipient_id=patient.id, content=Content(text=payload["message"]))
            messageFactory=Messages()
            response=messageFactory.PostNewMessage(newMessage)
            log=log+"bericht is verstuurd, "
            print("bericht is verstuurd ",response)
            return [self.statuses[2], log]

    def testTask(self, payload: list[dict[str:str]]) -> list[str]:
        print("-executing test task, payload:", payload)
        time.sleep(2)
        return [self.statuses[2], "succesvol getest"]
