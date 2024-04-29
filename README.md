# 🚧 PROJET/RAPPORT EN CONSTRUCTION/REDACTION 👷
https://docs.google.com/document/d/1Ki8N0ItqMbY1fsAPlTZ0nmYLW9LZNwK3USsC3wWIizU/edit
# Sommaire : 
- [DB]
- [Ajouter un deuxième service en local](#ajouter-un-deuxième-service-en-local) 
- [Ajouter une gateway en local](#ajouter-une-gateway-en-local) 
- [Ajouter un service en local](#ajouter-un-service-en-local) 
- [Déploiement](#déploiement) 
- [Utilisation](#utilisation) 

`
kubectl create secret generic mysql-secret \
  --from-literal=host='mysql' \
  --from-literal=username='flask' \
  --from-literal=password='password' \
  --from-literal=db='dbflask'
`
## MTLS
![[Pasted image 20240428234224.png]]
![[Pasted image 20240428234707.png]]

https://github.com/charroux/noops/tree/main/mysql#3-connexion-au-server-mysql

### Content Trust 
`export DOCKER_CONTENT_TRUST=1`  sur bashrc
- Lorsque vous poussez ou tirez des images, Docker signera et vérifiera automatiquement les images.

![[Pasted image 20240428235725.png]]
https://scout.docker.com/reports/org/chatodo/images
![[Pasted image 20240428235818.png]]
![[Pasted image 20240428235837.png]]


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
