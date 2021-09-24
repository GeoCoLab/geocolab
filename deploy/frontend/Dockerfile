FROM node:latest

COPY ./frontend/package.json /app/frontend/package.json
COPY ./frontend/yarn.lock /app/frontend/yarn.lock

WORKDIR /app/frontend

CMD yarn start
