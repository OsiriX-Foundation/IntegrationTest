#!/bin/bash

cd kheops
docker-compose down -v
docker-compose up -d
cd ..

./script_wait_docker_start.sh >/dev/null

docker ps -a
