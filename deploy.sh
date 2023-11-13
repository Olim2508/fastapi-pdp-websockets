#!/bin/sh

ssh -o StrictHostKeyChecking=no ec2-user@ec2-107-20-197-230.compute-1.amazonaws.com << 'ENDSSH'
  mkdir -p /home/ec2-user/ci-fastapi
  cd /home/ec2-user/ci-fastapi
  export $(cat .env | xargs)
#  docker login -u $CI_REGISTRY_USER -p $CI_JOB_TOKEN $CI_REGISTRY
#  docker pull $IMAGE:web
#  docker pull $IMAGE:nginx
#  docker-compose -f prod.ci.yml up -d
ENDSSH