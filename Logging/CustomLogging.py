import logging
from .loggingModels import *
from pathlib import Path
import atexit


class CustomLogging:
    def __init__(self) -> None:
        self.creationTime = datetime.now()
        # Set up the logger
        self.logger = logging.getLogger("myLogger")
        self.logger.setLevel(logging.DEBUG)  # Set the desired logging level

        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # file handler
        path = Path.cwd()
        log_directory = Path() / "Logging/log_directory"
        # Create directory if it doesn't exist
        log_directory.mkdir(parents=True, exist_ok=True)
        log_file_path = (
            log_directory
            / f'Log_created_at_{self.creationTime.strftime(r'%Y-%m-%d_%H-%M-%S')}.log'
        )
        log_file_path.touch(exist_ok=True)

        # create handler
        fileHandler = logging.FileHandler(log_file_path)
        fileHandler.setLevel(logging.DEBUG)

        # Create a formatter
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)
        fileHandler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(fileHandler)
        self.logMessages: list[LoggingMessage] = []
        self.Log(LoggingMessage("logfile created"))

    def cleanup(self) -> None:
        self.Log(LoggingMessage(message="program exiting"))

    def Log(self, loggingMessage: LoggingMessage):
        self.logMessages.append(loggingMessage)
        self.logger.debug(msg=loggingMessage.message)
