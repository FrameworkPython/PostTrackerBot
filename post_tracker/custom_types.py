
from pydantic import BaseModel, Field
from typing import List, Optional, TypedDict


class HourMinute(BaseModel):
    hour: int = Field(default=0, ge=0, le=23)
    minute: int = Field(default=0, ge=0, le=59)

    def __str__(self) -> str:
        return f"{self.hour:02}:{self.minute:02}"


class ShipmentStatus(BaseModel):
    index: int
    status: str
    location: str
    date: Optional[str]
    time: HourMinute


# TODO: not implemented yet
class ParcelInfo(TypedDict):
    key: str
    value: str


class TrackingResult(BaseModel):
    parcel_info: List[ParcelInfo] = []
    tracking_list: List[ShipmentStatus] = []
