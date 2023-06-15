FROM python:3.8

WORKDIR /owm_api

COPY requirements.txt /owm_api/requirements.txt
RUN pip install -r /owm_api/requirements.txt
COPY . /owm_api/

CMD 'uvicorn' 'app.main:app' '--reload' '--host' '0.0.0.0' '--port' '80'
