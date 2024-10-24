class Settings:
    def __init__(self) -> None:
        self.statuses: list[str] = [
            "in_queue",
            "processing",
            "completed",
            "failed",
        ]
        #delay in seconds
        self.maindelay = 0.01
        self.standbyDelay=3
        self.maxRetries=20
