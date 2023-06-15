from datetime import datetime
from typing import List, Union

from fastapi import APIRouter

from app.dals.city_dal import CityDAL
from app.db.database import async_session
from app.db.schemas import CityTemperature, CityMain

router = APIRouter()


@router.post('/weather/{city}', tags=['API Endpoints'])
async def post_city(city: str):
    async with async_session() as session:
        async with session.begin():
            city_dal = CityDAL(session)
            return await city_dal.create_city(city)


@router.get('/last_weather', tags=['API Endpoints'], response_model=List[CityTemperature])
async def last_weather(search: Union[str, None] = None):
    async with async_session() as session:
        async with session.begin():
            city_dal = CityDAL(session)
            return await city_dal.get_cities(search)


@router.get('/city_stats', tags=['API Endpoints'], response_model=CityMain, response_model_exclude_none=True)
async def get_city_stats(city: str, from_date: datetime, to_date: datetime):
    async with async_session() as session:
        async with session.begin():
            city_dal = CityDAL(session)
            return await city_dal.city_stats(city, from_date, to_date)
