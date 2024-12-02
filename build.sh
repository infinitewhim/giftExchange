#!/bin/bash

# Build the image
# e.g. docker build --tag <registry_account>/gift-exchange-api:<version> .
docker build --tag mydockerregistry/gift-exchange-api:1.0.0 .

# Push the image to a registry
# docker push <registry_account>/gift-exchange-api:<1.0.0>  (better use a specific version instead of 'latest')
