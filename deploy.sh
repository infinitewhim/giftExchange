#!/bin/bash

# Deploy the service into a K8S cluster.
# We could use Helm charts for more complex cases, but here we just have a manifest folder to contain
# a yaml file which has Deployment and Service (Kind) for simplicity
kubectl apply -f manifests/deployment.yaml

# A. Need to update the image field accordingly in the yaml, for the image you pushed to registry
# B. Service(in K8s) has different types for exposing purposes. 
  # 1) default type is cluster IP, only accessible internally so we need to use tools like 
  #    Nginx Ingress or Istio as entry point to redirect the external traffic into the correct service
  # 2) or expose as 'NodePort' so we set up a few hosts as 'edge worker node' to receive 
  #    traffic, that is another approach
  # 3) if it's a public cloud K8s cluster(EKS, GKE etc), we can expose the Service type as 'LoadBalancer'
