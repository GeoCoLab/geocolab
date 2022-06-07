FROM node:latest

COPY ./frontend /app/frontend
COPY ./deploy/frontend/entrypoint /entrypoint

WORKDIR /app/frontend

ENTRYPOINT ["/bin/bash", "/entrypoint"]

CMD yarn dev
