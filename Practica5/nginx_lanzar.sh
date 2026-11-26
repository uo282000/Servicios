#!/bin/bash

docker run -d --rm --name nginx-video -p 80:80 -v $(pwd)/html:/usr/share/nginx/html nginx