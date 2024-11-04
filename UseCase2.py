from QueueProgramLoop import QueueProgramLoop
from unittests.TestManager import TestManager
from Logging.CustomLogging import CustomLogging


def main():
    logger = CustomLogging()
    queuemanager = QueueProgramLoop(logging=logger)
    queuemanager.main()


def unitTesting():
    testManagerFactory = TestManager()
    testManagerFactory.main()


if __name__ == "__main__":
    main()
    # unitTesting()
