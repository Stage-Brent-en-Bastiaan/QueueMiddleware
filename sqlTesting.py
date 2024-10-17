from SqlServerConnection import SqlServerConnection

def main():

    serverConnection=SqlServerConnection()

    # Fetch data
    firstQueueTask = serverConnection.getFirstQueueItem()

    # Print fetched data
    print("first task in the queue", firstQueueTask)

if __name__ == "__main__":
    main()