# README 


### Docker setup

1. `cp .example.env .env`
2. Set values in `.env` file
3. `docker compose up --build -d`


### Setup on new empty server

1. Create user: on vnc console: `adduser xyz`
2. add ssh key: `ssh-copy-id xyz@123.123.123.123`
3. add user to sudo group: `sudo usermod -a -G sudo xyz`
4. install docker: https://docs.docker.com/engine/install/debian/
5. install portainer: https://install.portainer.io/set-up-portainer
6. install loki plugin: https://grafana.com/docs/loki/latest/clients/docker-driver/
7. create networks: `docker network create traefik services tracing`
8. Create all stacks in [deployment/compose-stacks](deployment/compose-stacks) in portainer
9. Clone repo: `git clone git@bitbucket.org:baehre/team-e.git`
10. create .env file `cp .example.env .env` and set values
11. setup user backend
    1. `cp user-backend/user_backend/example.alembic.ini user-backend/user_backend/alembic.ini`
    2. set `sqlalchemy.url` in alembic.ini
12. start container: `docker compose up -d`
13. Setup user management database `docker exec -it user-management-api alembic upgrade head`
14. create API endpoints, by executing [the create_apis.py](deployment/create_apis.py) script. 