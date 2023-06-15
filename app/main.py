from fastapi import FastAPI
from app.routers.cities import router


app = FastAPI()
app.include_router(router)


@app.get('/', tags=['Main Page'])
async def main_page():
    return 'Welcome to OpenWeatherMap API. Here, you can follow the weather of any city in the world!' \
           ' But if we do not have data about your city, you can add it by yourself!'
