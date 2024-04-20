# 🚧 PROJET/RAPPORT EN CONSTRUCTION/REDACTION 👷
# Sommaire : 
- [Ajouter un deuxième service en local](#ajouter-un-deuxième-service-en-local) 
- [Ajouter une gateway en local](#ajouter-une-gateway-en-local) 
- [Ajouter un service en local](#ajouter-un-service-en-local) 
- [Déploiement](#déploiement) 
- [Utilisation](#utilisation) 
## Ajouter un deuxième service en local 
Le deuxième service, le frontend via Nginx. 
- `nginx/nginx.yml` : configuration de déploiement pour Kubernetes.
## Ajouter une gateway en local
Utilisation d'Istio pour la gateway
```yml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
	name: flask-gateway
spec:
	selector:
		istio: ingressgateway
	servers:
	- port:
		number: 80
		name: http
		protocol: HTTP
	  hosts:
	  - "*"
```
## Ajouter un service en local
Le service Flask est un API backend déployé sur Kubernetes, qui gère les données des produits. 
Il est configuré pour être accessible via un NodePort.
## Déploiement
#### Construction des images Docker (également présent sur [DockerHub](https://hub.docker.com/u/chatodo))
```
docker build -t flask-app:latest flask/
docker build -t frontend-nginx:latest nginx/
```
#### Déployer sur Kubernetes
```
kubectl apply -f flask/flask.yml
kubectl apply -f nginx/nginx.yml
```

## Utilisation
1. `./ingress-forward.sh` 
2. http://localhost:31380/
