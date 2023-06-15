from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float


class City(Base):
    __tablename__ = 'openweather_city'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    city = Column(String, unique=True)

    information = relationship('Information', back_populates='city')


class Information(Base):
    __tablename__ = 'openweather_info'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    temperature = Column(Float)
    atm_pressure = Column(Integer)
    wind_speed = Column(Float)
    record_time = Column(DateTime)
    city_name = Column(String, ForeignKey('openweather_city.city'))

    city = relationship('City', back_populates='information')
