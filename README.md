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
1. Go to the folder where you want to deploy the project (Зайдите в папку, в которой вы хотите развернуть проект).
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

## Available endpoints (Доступные эндпоинты):

- ```/weather/{city}```

city - name of the city. Adding a city to the database if it is not there. Добавление города в БД, если его там нет.

- ```/last_weather```

Returns a list of existing cities with the latest recorded temperature. You can specify an optional {search} parameter that will search for a partial match of city names. Возвращает список существующих городов с последней записанной температурой. Можно указать опциональный параметр search по которому будет произведён поиск на частичное совпадение названий городов. 

- ```/city_stats```

We get for the given city (passing the city as a query parameter) all the data for the specified period, as well as the average values ​​for this period. Получаем по заданному городу (передаём город в качестве query параметра) все данные за указанный период, а также средние значения за этот период.





