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
    id: int
    task_type: str
    payload: list[dict[str:str]]
    status: str
    statuslog: Optional[str] = None
    retries: int = 0
    priority: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    processed_at: Optional[datetime] = None

    def update_status(self, new_status: list[str]):
        self.status = new_status[0]
        self.statuslog=new_status[1]
        self.updated_at = datetime.now()
        self.retries = self.retries + 1

    def start_process(self):
        self.processed_at = datetime.now()
        settingsfactory = Settings()
        self.update_status([list(settingsfactory.statuses)[1],"verwerking is gestart"])
