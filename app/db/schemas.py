from datetime import datetime
from pydantic import BaseModel
from typing import List, Union


class InformationMain(BaseModel):
    temperature: str
    atm_pressure: str
    wind_speed: str
    record_time: datetime

    class Config:
        orm_mode = True


class CityCreate(BaseModel):
    city: str


class CityTemperature(BaseModel):
    city_name: str
    temperature: str

    class Config:
        orm_mode = True


class CityMain(CityCreate):
    id: int
    information: List[InformationMain] = []
    avg_temp: Union[float, None] = None
    avg_pressure: Union[float, None] = None
    avg_speed: Union[float, None] = None

    class Config:
        orm_mode = True