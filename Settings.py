class Settings:
    def __init__(self) -> None:
        self.statuses: list[str] = {
            "in_queue",
            "processing",
            "completed",
            "failed",
        }
        self.maindelay = 2
