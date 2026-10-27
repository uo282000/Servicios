#!/bin/bash

docker run --name basedatos \
  -e MYSQL_ROOT_PASSWORD=claveroot \
  -e MYSQL_USER=amigosuser \
  -e MYSQL_DATABASE=amigosdb \
  -e MYSQL_PASSWORD=amigospass \
  -v /home/uo282000/Servicios/Practica2.3/basedatos:/var/lib/mysql \
  --rm --network pruebas -d mariadb