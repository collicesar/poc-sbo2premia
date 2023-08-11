from typing import List
from pydantic import BaseModel, Field
from datetime import datetime

class EventbridgeEvent(BaseModel):
    version: str
    id: str
    detail_type: str = Field(alias='detail-type')
    source: str
    account: str
    time: datetime
    region: str

    @property
    def dd_metric_name(self) -> str :
        return None
    
    @property
    def dd_metric_value(self) -> int :
        return None

    @property
    def dd_tags(self) -> List[str] :
        return None
    
    def to_db_key(self) -> dict:
        return None
    
    def to_db_properties(self) -> dict:
        return None