import time
import traceback
from SQLQueueCommunication.SqlServerConnection import *
from SQLQueueCommunication.Models import *
from ApiCommunication.Messages import Messages
from ApiCommunication.Patienten import Patienten
from ApiCommunication.Models2 import *
from Settings import Settings
from LoggingHelpers.Logging import CustomLogging

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
        self.standbyDelay=settings.standbyDelay
        self.logFactory=CustomLogging()

    # het programmaverloop
    def main(self):
        teller = 0
        amountofloops = 2
        running = True
        # program loop
        while running:
            self.action()
            # wacht
            time.sleep(self.delay)
            if teller >= amountofloops - 1:
                running = False
                self.logFactory.Log("ending queueprogram main program loop")
            teller = teller + 1

    # 1 actie van de queueManager
    def action(self):
        #maak de connectie aan
        serverConnection=None
        try:
            serverConnection = SqlServerConnection()
        except Exception as e:
            self.logFactory.Log(traceback.format_exc(),"probleem met de databaseconnectie:")
        # get the Task uit de queue
        firstQueueTask=None
        try:
            firstQueueTask = serverConnection.getNextQueueItem()
        except Exception as e:
            self.logFactory.Log(traceback.format_exc(),"er ging iets mis bij het opvragen van de task uit de queue")

        #als er geen task is gevonden(alles is afgehandeld) ga in standby modus anders wordt de gevonden task afgehandeld
        if (firstQueueTask == None):
            self.logFactory("geen task gevonden")
            time.sleep(self.standbyDelay)
            pass
        else:
            self.handleTask(firstQueueTask)

    # behandeld de doorgestuurde task
    def handleTask(self, task: Task) -> None:
        self.logFactory.Log("task gevonden")
        task.start_process()
        conn = SqlServerConnection()
        conn.updateTask(task)
        # get the function from taskdict that is linked to the task type name and execute it if it exists,
        functionToExecute: list[str] = self.taskDict.get(task.task_type)
        statusToUpdate = None
        if functionToExecute == None:
            statusToUpdate = [self.statuses[3], "dit task type wordt niet ondersteund"]
            self.logFactory.Log(traceback.format_exc(),"dit task type wordt niet ondersteund",task.task_type)
        else:
            try:
                statusToUpdate = functionToExecute(task.payload)
            except Exception as e:
                statusToUpdate=[self.statuses[3], f"er ging iets mis bij het uitvoeren van de task: {traceback.format_exc()}"]
                self.logFactory.Log(traceback.format_exc(),"er ging iets mis bij het uitvoeren van de task")
                
            
        # return the returned status to the update_status method
        task.update_status(statusToUpdate)
        conn.updateTask(task)

    # taskdict methods, should all look the same
    def sendMessage(self, payload) -> list[str]:
        log = ""
        print("-executing send message task, payload:", payload)
        # check wether payload is the correct type
        if not isinstance(payload, dict):
            self.logFactory.Log("foutieve payload in de task")
            return (
                self.statuses[3],
                """foutieve payload: geef een juiste payload terug de payload voor send_message moet er zo uitzien { "patient_number":"7402241006","message":"Graag je huisarts contacteren voor meer info"}""",
            )
        payload: dict[str, str] = payload

        # get the patient from the bewell api
        patientenFactory = Patienten()
        hospitalId = payload["hospital_id"]
        self.logFactory.Log(hospitalId,"searching for patient met hospital_id: ")
        patient = patientenFactory.getPatientHospitalId(hospitalId)
        # als er geen patient gevonden is geef een gepaste status en statuslog mee
        if patient == None:
            self.logFactory.Log("deze patient bestaat niet in de bewell omgeving")
            return [self.statuses[3], "deze patient bestaat niet in de bewell omgeving"]
        else:
            print("patient gevonden: ", patient)
            log = log + "patient is gevonden, "
            # verstuur message naar de gevonden patient
            newMessage = MessagePost(
                recipient_id=patient.id, content=Content(text=payload["message"])
            )
            messageFactory = Messages()
            response = messageFactory.PostNewMessage(newMessage)
            log = log + "bericht is verstuurd, "
            self.logFactory.Log(response,"bericht is verstuurd ")
            return [self.statuses[2], log]

    def testTask(self, payload: list[dict[str:str]]) -> list[str]:
        self.logFactory.Log(payload,"-executing test task, payload:")
        time.sleep(2)
        return [self.statuses[2], "succesvol getest"]
