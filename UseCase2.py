from QueueManager import QueueManager
from unittests.TestManager import TestManager
from Logging.CustomLogging import CustomLogging


def main():
    logger=CustomLogging()
    queuemanager = QueueManager(logger=logger)
    queuemanager.main()


def unitTesting():
    testManagerFactory = TestManager()
    testManagerFactory.main()


if __name__ == "__main__":
    main()
    # unitTesting()
