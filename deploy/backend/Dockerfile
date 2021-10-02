FROM python:latest

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  python3-dev \
  postgresql-client

COPY ./deploy/backend/entrypoint /entrypoint
COPY . /app

WORKDIR /app

RUN python setup.py develop

ENTRYPOINT ["/bin/bash", "/entrypoint"]

CMD flask run --host 0.0.0.0 --port 8000

