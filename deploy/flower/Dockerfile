FROM python:3.9

RUN apt-get update -y

COPY ./backend/requirements.txt /deploy/requirements.txt
COPY ./deploy/flower/config/flowerconfig.py /config/flowerconfig.py
RUN pip install -r /deploy/requirements.txt
RUN pip install flower

WORKDIR /app/backend

CMD celery --app geocolab.celery_worker flower -l INFO --conf=/config/flowerconfig.py
