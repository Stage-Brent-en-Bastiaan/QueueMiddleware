from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any

@dataclass
class TaskType:
    task_type: str
    description: Optional[str] = None
    api_endpoint: Optional[str] = None

@dataclass
class TaskQueue:
    id: int
    task_type: str
    payload: Any
    status: str
    statuslog: Optional[str] = None
    retries: int = 0
    priority: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    processed_at: Optional[datetime] = None

    def update_status(self, new_status: str):
        self.status = new_status
        self.updated_at = datetime.now()
