# IBISAI resultlist service
# python resultlist.py install
 
import datetime
import socket
import time
import win32serviceutil
import win32service
import win32event
import servicemanager
 
class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "_tempservice4"  # Geef een naam aan je service
    _svc_display_name_ = "_tempservice4"  # Geef een weergavenaam aan je service
    _svc_description_ = "_tempservice4"  # Geef een beschrijving van je service
 
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)  # Set default timeout for socket operations
        self.is_running = True
 
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False
 
    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
        self.main()
        self.is_running = True
 
    def main(self):
        # Voeg hier de logica van je service toe (bijvoorbeeld de code voor het verwerken van de queue-items)
        # Dit is de plek waar je je bestaande code moet plaatsen om de functionaliteit uit te voeren.
 
        # logging.info(datetime.datetime.now().strftime("%Y%m%d%H%M%S") + " - Start processing")
 
        while self.is_running:
            # Plaats hier de logica van je service die continu blijft draaien (bijv. het verwerken van de queue)
 
            # hour = int(datetime.datetime.now().strftime("%H"))
            #if hour < 20 or hour > 7:
            #    time.sleep(5)  # Wacht 5 seconde
            #else:
            time.sleep(1)
               
            # Ophalen van patiënten met status 1
            pass
 
        # logging.info(datetime.datetime.now().strftime("%Y%m%d%H%M%S") + " - Stop processing")
 
if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MyService)
 
#if __name__ == "__main__":
#    process_queue_from_database()