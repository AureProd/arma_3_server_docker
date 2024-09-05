# Arma 3 server

To build `arma:latest` image

```bash
docker build -t arma:latest .
```

---

Exemple of docker compose 

```yml
services:
    server:
        image: arma:latest
        restart: always
        environment:
            STEAM_USER: steam_user
            STEAM_PASSWORD: ************
            ADMIN_PASSWORD: ************
            ARMA_PARAMS: -autoinit
            MYSQL_HOST: db
            MYSQL_PORT: 3306
            MYSQL_DATABASE: database
            MYSQL_USER: superadmin
            MYSQL_PASSWORD: ************
        ports:
            - 2302-2306:2302-2306/udp
        volumes:
            - ./build:/server
            - ./configs/mpmissions:/configs/mpmissions
            - ./configs/servermods:/configs/servermods
            - ./configs/mods.json:/configs/mods.json
            - ./configs/server.cfg:/configs/server.cfg
```