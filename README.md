# API service that collects information from openweathermap.
# Сервис API, который собирает информацию из openweathermap.
## The service is asynchronous, it collects data based on user requests, writing cities to the database, after which, every 10 minutes, a parser written in scrapy is launched, which collects information about the weather in cities.
## Сервис асинхронный, собирает данные исходя из запросов пользователей, записывая города в БД, после чего, каждые 10 минут запускается парсер, написанный на scrapy, который коллекционирует информацию о погоде в городах.

Used technologies (Использованные технологии):
- FastAPI
- Async Postgres
- Scrapy
- Alembic
- SQLAlchemy
- uvicorn
