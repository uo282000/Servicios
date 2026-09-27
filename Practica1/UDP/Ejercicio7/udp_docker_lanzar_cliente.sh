#!/bin/bash

# Lanzamos al cliente
docker run -it --network pruebas --name cliente -v $(pwd):/app python:3.7    python /app/udp_cliente6_broadcast.py

