from dataclasses import dataclass
from datetime import datetime
import traceback
from typing import Optional


@dataclass
class LoggingMessage:
    message: str
    source: str = traceback.format_exc()
    title: str = ""
    logLevel: int = 1
    timestamp: datetime = datetime.now()
    metaData: Optional[str] = ""

    # private props
    _loglevelNameDict = {0: "info", 1: "debugging", 2: "warning", 3: "error"}

    def logLevelName(self) -> str:
        return self.loglevelNameDict.get(self.logLevel)

    def __str__(self) -> str:
        return f"{self.timestamp}: {self.message}"
