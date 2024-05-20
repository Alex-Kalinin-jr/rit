from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class GroupType(str, Enum):
    day = "day"
    month = "month"
    hour = "hour"

class MessageData(BaseModel):
    dt_from: datetime
    dt_upto: datetime
    group_type: GroupType
