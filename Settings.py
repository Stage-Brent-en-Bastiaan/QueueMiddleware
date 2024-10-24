class Settings:
    def __init__(self) -> None:
        self.statuses: list[str] = [
            "in_queue",
            "processing",
            "completed",
            "failed",
        ]
        #delay in seconds
        self.maindelay = 1
        self.standbyDelay=3
        self.maxRetries=20
        self.maxPriority=100
