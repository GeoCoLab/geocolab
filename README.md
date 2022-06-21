# GeoCoLab

## About GeoCoLab

_GeoCoLab_ is a project responding to the NERC Digital Technologies Digital Sprint. It aims to evidence and address the hypothesis that access to analytical facilities by underserved researchers is a key issue that leads to a deep inequality in environmental research and determines who is able to generate environmental and geoscience knowledge.

A proposed solution to this issue is an online collaborative platform, _GeoCoLab_, that would link underserved researchers with laboratory facilities who have agreed to offer a quota of pro bono services. This platform would match researcher need and facility anonymously, initially protecting both parties, and will facilitate ethical collaboration agreements. 

## Development

### Requirements
- [Docker Compose](https://docs.docker.com/compose)

### Quickstart
Clone the repository, including the submodules:
```shell
git clone --recurse-submodules https://github.com/GeoCoLab/geocolab.git
```

Start the containers (`-d` starts them in the background):
```shell
docker compose up -d
```

On first run, the database will also need to be initialised:
```shell
docker compose exec backend python -m geocolab.cli db init
docker compose exec backend python -m geocolab.cli db upgrade
```

Then the admin user should be created:
```shell
docker compose exec backend python -m geocolab.cli make-admin
```

The site should then be available at [http://10.0.12.12](http://10.0.12.12).

### Structure
- Backend: [Flask](https://flask.palletsprojects.com)
- Frontend: [Vite](https://vitejs.dev), [vite-plugin-ssr](https://vite-plugin-ssr.com), and [Vue 3](https://vuejs.org)
- Database: [PostgreSQL](https://www.postgresql.org)
- Server: [NGINX](https://www.nginx.com)
- Other: [Celery](https://docs.celeryq.dev), [Redis](https://redis.io), [RabbitMQ](https://www.rabbitmq.com), and [Flower](https://flower.readthedocs.io)

### Additional commands
When a change has been made to the database models, migrations need to be regenerated and applied:
```shell
docker compose exec backend python -m geocolab.cli db migrate
docker compose exec backend python -m geocolab.cli db upgrade
```


