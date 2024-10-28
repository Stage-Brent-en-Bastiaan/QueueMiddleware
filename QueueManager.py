import time
import traceback
from SQLQueueCommunication.SqlServerConnection import *
from SQLQueueCommunication.Models import *
from BewellApiCommunication.Messages import Messages
from BewellApiCommunication.Patienten import Patienten
from BewellApiCommunication.Models2 import *
from Settings import Settings
from Logging.CustomLogging import CustomLogging
from Logging.loggingModels import *


class QueueManager:
    def __init__(self) -> None:
        # dit zijn alle types van tasks de kunnen uitgevoerd worden: ze worden gelinkt aan een methode
        settings = Settings()
        self.taskDict: dict[str, function] = {
            "send_message": self.sendMessage,
            "test_task": self.testTask,
        }
        self._statuses = list(settings.statuses)
        self.delay = settings.maindelay
        self.standbyDelay = settings.standbyDelay
        self._logFactory = CustomLogging()
        self.active = False

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
            # if teller >= amountofloops - 1:
            #     running = False
            #     self.logFactory.Log("ending queueprogram main program loop")
            # teller = teller + 1

    # 1 actie van de queueManager
    def action(self):
        # maak de connectie aan
        serverConnection = None
        try:
            serverConnection = SqlServerConnection()
        except Exception as e:
            self._logFactory.Log(
                loggingMessage=LoggingMessage(
                    "er kon geen verbinding gemaakt worden met de database",
                    traceback.format_exc(),
                )
            )
            self.standBy()

        # get the Task uit de queue
        firstQueueTask = None
        try:
            firstQueueTask = serverConnection.getNextQueueItem()
        except Exception as e:
            self._logFactory.Log(
                loggingMessage=LoggingMessage(
                    "er ging iets mis bij het opvragen van de task uit de queue",
                    traceback.format_exc(),
                )
            )

        # als er geen task is gevonden(alles is afgehandeld) ga in standby modus anders wordt de gevonden task afgehandeld
        if firstQueueTask == None:
            self._logFactory.Log(
                LoggingMessage("geen task gevonden", traceback.format_exc())
            )
            self.standBy()
            pass
        else:
            self.activate()
            self.handleTask(firstQueueTask)

    # als er niets wordt gevonden
    def standBy(self):
        if self.active == True:
            self._logFactory.Log(LoggingMessage("standing by", traceback.format_exc()))
            self.active = False
        time.sleep(self.standbyDelay)

    def activate(self):
        if self.active == False:
            self._logFactory.Log(LoggingMessage("activating", traceback.format_exc()))
            self.active = True
    def updateTask(self,logmessage:LoggingMessage):
        pass
    # behandeld de doorgestuurde task
    def handleTask(self, task: Task) -> None:
        self._logFactory.Log(
            LoggingMessage(
                f"task wordt behandelt met id: {task.id}", traceback.format_exc()
            )
        )
        task.start_process()
        conn = SqlServerConnection()
        conn.updateTask(task)
        # get the function from taskdict that is linked to the task type name and execute it if it exists,
        functionToExecute: list[str] = self.taskDict.get(task.task_type)
        statusToUpdate = None
        if functionToExecute == None:
            statusToUpdate = [self._statuses[3], "dit task type wordt niet ondersteund"]
            self._logFactory.Log(
                LoggingMessage(
                    f"dit task type wordt niet ondersteund: {task.task_type}",
                    traceback.format_exc(),
                )
            )
        else:
            try:
                statusToUpdate = functionToExecute(task.payload)
            except Exception as e:
                statusToUpdate = [
                    self._statuses[3],
                    f"er ging iets mis bij het uitvoeren van de task: {traceback.format_exc()}",
                ]
                self._logFactory.Log(
                    LoggingMessage(
                        "er ging iets mis bij het uitvoeren van de task",
                        traceback.format_exc(),
                    )
                )

        # return the returned status to the update_status method
        task.update_status(statusToUpdate)
        conn.updateTask(task)
    

    # taskdict methods, should all look the same
    def sendMessage(self, payload) -> list[str]:
        log = ""
        self._logFactory.Log(
            LoggingMessage(
                f"-executing send message task",
                traceback.format_exc(),
            )
        )
        # check wether payload is the correct type
        if not isinstance(payload, dict):
            self._logFactory.Log(
                LoggingMessage("foutieve payload in de task", traceback.format_exc())
            )
            return (
                self._statuses[3],
                """foutieve payload: geef een juiste payload terug de payload voor send_message moet er zo uitzien { "patient_number":"7402241006","message":"Graag je huisarts contacteren voor meer info"}""",
            )
        payload: dict[str, str] = payload

        # get the patient from the bewell api
        patientenFactory = Patienten()
        hospitalId = payload["hospital_id"]
        self._logFactory.Log(
            LoggingMessage(
                f"searching for patient met hospital_id: {hospitalId}",
                traceback.format_exc(),
            )
        )
        patient = patientenFactory.getPatientHospitalId(hospitalId)
        # als er geen patient gevonden is geef een gepaste status en statuslog mee
        if patient == None:
            self._logFactory.Log(
                LoggingMessage(
                    "deze patient bestaat niet in de bewell omgeving",
                    traceback.format_exc(),
                    logLevel=3,
                )
            )
            return [
                self._statuses[3],
                "deze patient bestaat niet in de bewell omgeving",
            ]
        else:
            self._logFactory.Log(
                LoggingMessage(
                    f"patient gevonden met id: {patient.id}", traceback.format_exc()
                )
            )
            log = log + f"patient gevonden met id: {patient.id}"
            # verstuur message naar de gevonden patient
            message=payload["message"]
            title=payload["title"]
            content=Content( text=message,title=title)
            filepayload:list[dict] =payload.get("files")
            files:list[File] = []
            for file in filepayload:
                filename=file["filename"]
                data=file["data"]
                file=File(filename=filename,data=data)
                files.append(file)
            newMessage = MessagePost(
                recipient_id=patient.id, 
                content=content,
                files=files
            )
            messageFactory = Messages()
            response = messageFactory.PostNewMessage(newMessage)
            log = log + f"bericht is verstuurd, id van verstuurde message: {response} "
            self._logFactory.Log(
                LoggingMessage(f"bericht is verstuurd, id van verstuurde message: {response}")
            )
            return [self._statuses[2], log]

    def testTask(self, payload: list[dict[str:str]]) -> list[str]:
        self._logFactory.Log(
            LoggingMessage(f"executing test task, payload: {payload}"),
            traceback.format_exc(),
        )
        time.sleep(2)
        return [self._statuses[2], "succesvol getest"]
