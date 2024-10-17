from QueueInteraction.SqlServerConnection import SqlServerConnection
import time
def main():
    running=True
    while(running):
        serverConnection=SqlServerConnection()

        # Fetch data
        firstQueueTask = serverConnection.getFirstQueueItem()

        # Print fetched data
        print("first task in the queue", firstQueueTask)
        #wacht 5 seconden
        time.sleep(5)
if __name__ == "__main__":
    main()