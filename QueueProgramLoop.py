import time
import traceback
from Logging.loggingModels import LoggingMessage
from MiddleWare.QueueManager import QueueManager
from Settings import Settings
from Logging.CustomLogging import CustomLogging


class QueueProgramLoop:
    def __init__(self, logging: CustomLogging) -> None:
        # --logging--
        self.logger = logging

        # --settings--
        settings = Settings()
        self.delay = settings.maindelay
        self.standbyDelay = settings.standbyDelay
        self.active=False

    def main(self)->None:
        # teller = 0
        # amountofloops = 2
        running = True
        queuemanager = QueueManager(self.logger)
        # program loop
        while running:
            response = queuemanager.action()
            if response == "active":
                self.activate()
            else:
                self.standBy()
            # wacht

            # if teller >= amountofloops - 1:
            #     running = False
            #     self.logFactory.Log("ending queueprogram main program loop")
            # teller = teller + 1

    # als er niets wordt gevonden
    def standBy(self):
        if self.active == True:
            self._logFactory.Log(LoggingMessage("standing by", traceback.format_exc()))
            self.active = False
        time.sleep(self.standbyDelay)

    #als er een task gevonden is
    def activate(self):
        if self.active == False:
            self._logFactory.Log(LoggingMessage("activating", traceback.format_exc()))
            self.active = True
        time.sleep(self.delay)
