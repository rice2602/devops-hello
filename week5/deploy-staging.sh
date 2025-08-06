#!/bin/bash
docker pull rice2602/week5-web:staging
docker compose -f docker-compose.staging.yml up -d
