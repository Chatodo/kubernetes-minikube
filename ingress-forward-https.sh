#!/bin/sh
echo Open Ingress at https://localhost:31380/
kubectl -n istio-system port-forward deployment/istio-ingressgateway 31380:8443