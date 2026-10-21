#!/bin/bash

docker run --rm -d --network pruebas \
   --name nginx -p 80:80 -p 81:81 \
   -v /home/uo282000/Servicios/Practica2/html:/usr/share/nginx/html \
   -v /home/uo282000/Servicios/Practica2/html2:/usr/share/nginx/html2 \
   -v /home/uo282000/Servicios/Practica2/sitios_nginx:/etc/nginx/conf.d nginx