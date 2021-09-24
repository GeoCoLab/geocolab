FROM python:3.8

RUN apt-get update -y

COPY ./backend/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /app/backend

CMD celery --app geocolab.celery_worker worker
