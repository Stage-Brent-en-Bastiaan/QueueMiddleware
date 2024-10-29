import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import os
import time
from QueueManager import QueueManager
from Settings import Settings
import threading


class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "api_communication_middleWare_azstlucas_brent_bastiaan_mario"
    _svc_display_name_ = "api_communication_middleWare_azstlucas_brent_bastiaan_mario"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(120)
        self.is_alive = True
        queueManager=QueueManager()
        self.settings=Settings()
        self.threads:list[threading.Thread]=[threading.Thread(target=queueManager.main)]

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False
        for thread in self.threads:
            thread.join()

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, ""),
        )
        self.main()

    def main(self):
        # Main service logic goes here
        for thread in self.threads:
            thread.start()
        #self.thread2.start()
        while self.is_alive:
            # Perform your service tasks here
            win32event.WaitForSingleObject(self.hWaitStop, 500)


if __name__ == "__main__":
    if len(os.sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MyService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MyService)
