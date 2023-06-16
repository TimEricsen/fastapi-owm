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

How to run localy (Как локально запустить):
1. Go to the folder in which to deploy the project (Зайдите в папку, в которой развернуть проект).
2. Run the command (Запустите команду):
```git init```
3. Then run the command below, to copy this project to your machine (Затем выполните приведенную ниже команду, чтобы скопировать этот проект на свой компьютер.):
```git clone https://github.com/TimEricsen/fastapi-owm.git```
4. Then go to project folder (Затем перейдите в папку проекта):
```cd fastapi-owm```
5. Now you can run the docker-compose command to create the container (Теперь вы можете запустить команду docker-compose для создания контейнера.):
```docker-compose up -d --build```

After the steps taken, the container will be created and available for use.
После проделанных шагов, контейнер будет создан и доступен для использования.
