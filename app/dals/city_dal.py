import os
import requests

from typing import Union
from dotenv import load_dotenv

from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.future import select
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status, Response

from app.db.models import City, Information
from app.db.schemas import CityTemperature, CityMain, InformationMain
from app.routers.dependencies import get_parameters


class CityDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_city(self, city: str):
        parameters = get_parameters()
        parameters['q'] = city
        db_city = await self.db_session.execute(select(City).where(City.city == city.title()))
        db_city = db_city.first()

        if db_city:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='This city is already in our database!'
            )

        try:
            load_dotenv()
            url = os.getenv('URL')
            request_try = requests.get(url=url, params=parameters).json()

            if request_try['cod'] == '404':
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Please, write the right name of the city!'
                )

            new_city = City(city=city.title())
            self.db_session.add(new_city)
            await self.db_session.flush()
            return Response(
                status_code=status.HTTP_201_CREATED,
                content='This city wasn`t in our data, but we`ve already added it. Thanks!'
                        ' Information about this city will be available soon!'
            )

        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Please, write the right name of the city!'
            )

    async def get_cities(self, search: Union[str, None] = None):
        if not search:
            cities = await self.db_session.execute(select(City))
            result = []
            for city in cities.all():
                city_info = await self.db_session.execute(select(Information).where(
                    Information.city_name == city[0].city).order_by(Information.record_time.desc()))
                first_info = city_info.first()
                if not first_info:
                    continue
                city_to_json = jsonable_encoder(first_info)
                city_to_api = CityTemperature(**city_to_json.get('Information'))
                result.append(city_to_api)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Data has no any city yet!'
                )
            return result

        else:
            cities = await self.db_session.execute(select(City).where(City.city.like(f'{search.capitalize()}%')))
            cities = cities.all()
            if not cities:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='There is no any city with name like this'
                )

            result = []
            for city in cities:
                city_info = await self.db_session.execute(select(Information).where(
                    Information.city_name == city[0].city).order_by(Information.record_time.desc()))
                first_info = city_info.first()
                if not first_info:
                    continue
                city_to_json = jsonable_encoder(first_info)
                city_to_api = CityTemperature(**city_to_json.get('Information'))
                result.append(city_to_api)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='No data has been collected for this city(cities) yet!'
                )
            return result

    async def city_stats(self, city: str, from_date: datetime, to_date: datetime):
        if from_date > to_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='First date must be smaller than second!'
            )

        db_city = await self.db_session.execute(select(City).where(City.city == city).options(
            selectinload(City.information)))
        db_city = db_city.scalars().first()

        if not db_city:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='City with this name not found! City name is case sensitive!'
            )

        if not db_city.information:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Data for this city has not yet been collected. Please try again in a few minutes!'
            )

        ans_city = CityMain(**jsonable_encoder(db_city))
        db_info = await self.db_session.execute(select(Information).where(
            Information.record_time >= from_date, Information.record_time <= to_date, Information.city_name == city))
        db_info = db_info.scalars().all()

        if not db_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='There is no date in the range you specified! You may have entered the wrong date!'
            )
        if len(db_info) == 1:
            ans_info = InformationMain(**jsonable_encoder(db_info[0]))
            ans_city.information = [ans_info]
            return ans_city

        avg_temp = await self.db_session.execute(select(func.avg(Information.temperature)).where(
            Information.record_time >= from_date, Information.record_time <= to_date, Information.city_name == city))
        avg_temp = avg_temp.scalar()

        avg_pressure = await self.db_session.execute(select(func.avg(Information.atm_pressure)).where(
            Information.record_time >= from_date, Information.record_time <= to_date, Information.city_name == city))
        avg_pressure = avg_pressure.scalar()

        avg_speed = await self.db_session.execute(select(func.avg(Information.wind_speed)).where(
            Information.record_time >= from_date, Information.record_time <= to_date, Information.city_name == city))
        avg_speed = avg_speed.scalar()

        result_info = []
        for info in db_info:
            result_info.append(InformationMain(**jsonable_encoder(info)))

        ans_city.information = result_info
        ans_city.avg_temp = round(avg_temp, 2)
        ans_city.avg_pressure = round(avg_pressure, 2)
        ans_city.avg_speed = round(avg_speed, 2)

        return ans_city
