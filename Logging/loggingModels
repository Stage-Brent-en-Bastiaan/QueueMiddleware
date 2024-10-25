from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class LoggingMessage():
    timestamp:datetime=datetime.now()
    logLevel: Optional[int]=0
    title:Optional[str]
    message:str
    source:str
    metaData:Optional[str]
    _loglevelNameDict={0:"info",1:"debugging",2:"warning",3:"error"}
    def logLevelName(self)->str:
        return self.loglevelNameDict.get(self.logLevel) 
    def __str__(self) -> str:
        return f"{self.timestamp}: {self.message}"
