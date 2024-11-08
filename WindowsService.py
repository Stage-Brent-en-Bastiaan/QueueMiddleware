import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import os
import subprocess
import QueueProgramLoop
# from Settings import Settings
from Logging.CustomLogging import CustomLogging
from Logging.CustomLogging import LoggingMessage


class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "_api_debug"
    _svc_display_name_ = "_api_debug"

    def __init__(self, args):
        # self.logger = CustomLogging()
        # self.logger.Log("service created")
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(120)
        self.is_alive = True
        self.uwsgi_process = None

        # queueManager = QueueManager(self.logger)
        # self.settings = Settings()
        # self.threads: list[threading.Thread] = [
        #     threading.Thread(target=queueManager.main),
        #     threading.Thread(target=self.startUwsgi),
        # ]
        # os.environ["DJANGO_SETTINGS_MODULE"] = (
        #     "django_react.settings"  # Adjust as necessary
        # )

    def SvcStop(self):
        # self.logger.Log("service stopping")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False
        if self.uwsgi_process:
            self.uwsgi_process.terminate()  # Gracefully terminate the uWSGI process
            self.uwsgi_process = None

    def SvcDoRun(self):
        # self.logger.Log("service starting")
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, ""),
        )
        self.main()

    def main(self):
        # self.logger.Log("entering main")
        # Main service logic goes here
        # for thread in self.threads:
        #     thread.start()
        # self.thread2.start()
        while self.is_alive:
            servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, "entering main program loop"),
            )
            # Perform your service tasks here
            # queueProgramLoop:QueueProgramLoop = QueueProgramLoop(self.logger)
            # queueProgramLoop.main()
            win32event.WaitForSingleObject(self.hWaitStop, 500)

    def startUwsgi(self):
        self.uwsgi_process = subprocess.Popen(
            ["uwsgi", "--ini", "uwsgi.ini"],  # Adjust the path as necessary
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )


if __name__ == "__main__":
    logger = CustomLogging()
    logger.Log(LoggingMessage(message=os.getcwd()))
    if len(os.sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MyService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MyService)
