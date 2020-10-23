#!/bin/bash

cd kheops
docker-compose down -v
docker-compose up -d
cd ..
sleep 60
docker ps -a
