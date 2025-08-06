#!/bin/bash
docker pull rice2602/week5-web:latest
docker compose -f docker-compose.prod.yml up -d
