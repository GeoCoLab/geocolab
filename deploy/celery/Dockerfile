FROM python:3.9

RUN apt-get update -y

COPY ./backend/requirements.txt /deploy/requirements.txt
RUN pip install -r /deploy/requirements.txt

WORKDIR /app/backend

CMD celery --app geocolab.celery_worker worker
