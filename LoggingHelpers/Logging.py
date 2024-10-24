import logging

class CustomLogging:
    def __init__(self) -> None:
        # Set up the logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)  # Set the desired logging level
        
        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        
        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        # Add the handler to the logger
        self.logger.addHandler(console_handler)

    def Log(self,inhoud:str,title="",priority=1):
        print(title,inhoud,sep=" ")