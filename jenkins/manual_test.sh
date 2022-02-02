#!/usr/bin/env bash

DOCKER_ORGANIZATION_NAME="isstech"
SERVICE_NAME="issassist"
GIT_ORGANIZATION_NAME="IssTech"
DOCKER_REGISTRY="$DOCKER_ORGANIZATION_NAME/$SERVICE_NAME"
PROD_NAMESPACE="issassist-prod"
PROD_URL="issassist.isstech.local"
GIT_BRANCH="latest"
TEST_NAMESPACE="issassist-test"
TEST_URL="issassist-test.isstech.local"
ANNOTATIONS="kubernetes.io/ingress.class: traefik"

function deploy {
  echo 'export ANNOTATIONS="kubernetes.io/ingress.class: traefik"'
  echo helm install $SERVICE_NAME ../deployment/helm/ \
  --set ingress.enabled=True \
  --set ingress.hosts[0].host=$PROD_URL \
  --set ingress.hosts[0].paths[0].path=/ \
  --set ingress.hosts[0].paths[0].pathType=ImplementationSpecific  \
  --set ingress.metadata.annotations=ANNOTATIONS \
  --set issassist.backend.image.tag=$GIT_BRANCH \
  --set issassist.backend.image.pullPolicy=Always \
  --namespace=$PROD_NAMESPACE \
  --create-namespace \
  --wait
}

function test  {
   curl $TEST_URL
}

deploy
test
