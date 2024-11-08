class Settings:
    def __init__(self) -> None:
        self.statuses: dict[str:str] = {
            "in_queue": "in_queue",
            "processing": "processing",
            "completed": "completed",
            "failed": "failed",
        }
        # delay in seconds
        self.maindelay = 1
        self.standbyDelay = 3
        self.maxPriority = 100
