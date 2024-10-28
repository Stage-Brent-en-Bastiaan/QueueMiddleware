from QueueManager import QueueManager
from unittests.TestManager import TestManager
import time


def main():
    queuemanager = QueueManager()
    queuemanager.main()
def unitTesting():
    testManagerFactory=TestManager()
    testManagerFactory.main()

if __name__ == "__main__":
    main()
    #unitTesting()
