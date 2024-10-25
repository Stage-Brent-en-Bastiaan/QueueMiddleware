from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any
from Settings import Settings


@dataclass
class TaskType:
    task_type: str
    description: Optional[str] = None
    api_endpoint: Optional[str] = None


@dataclass
class Task:
    id: Optional[int]
    task_type: str
    payload: any
    status: str
    statuslog: Optional[str] = ""
    retries: int = 0
    priority: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    processed_at: Optional[datetime] = None
    logTeller: Optional[int] = 0

    def update_status(self, new_status: list[str]):
        if new_status is None:
            raise ValueError("new_status cannot be None")
        self.status = new_status[0]
        self.statuslog = self.statuslog + f"{self.logTeller}: {new_status[1]} "
        self.logTeller = self.logTeller + 1
        self.updated_at = datetime.now()

    def start_process(self):
        self.processed_at = datetime.now()
        settingsfactory = Settings()
        self.update_status([list("attempt", f"{self.retries}")])
        self.retries = self.retries + 1
