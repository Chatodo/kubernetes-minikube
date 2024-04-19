# 🚧 PROJET/RAPPORT EN CONSTRUCTION/REDACTION 👷
---
# Sommaire : 
[[#Ajouter une gateway en local (12/20)]]

---
## Ajouter une gateway en local (12/20)
**Composition du projet :**
- **Flask**
- **Docker**
- **Kubernetes**
- **Istio(Service mesh)**
### Liste des fichiers
**`flask/flask.yml`**
Configuration et du déploiement de l'application Flask sur Kubernetes. 
- **Deployment**: Configure un déploiement Kubernetes pour l'application Flask, spécifiant deux réplicas Le déploiement utilise l'image Docker `chatodo/flask-api:latest` et expose l'application sur le port 5000.
- **Service**: Définit un service de type `ClusterIP` qui permet d'accéder à l'application Flask à l'intérieur du cluster Kubernetes. Ce service écoute sur le port 5000 et route le trafic vers les pods Flask.
- **Gateway**: Configure une Gateway Istio pour exposer l'application Flask à l'extérieur du cluster. La Gateway écoute sur le port 80 (HTTP) et accepte toutes les requêtes venant de n'importe quel hôte (`"*"`)

**`nginx/nginx-deployment.yml`**
Déploiement et l'exposition du service Nginx à l'aide de Kubernetes et Istio
- **VirtualService**: Définit un VirtualService Istio qui route le trafic entrant vers l'application Flask. Il spécifie que toutes les requêtes avec le préfixe URI `/api` doivent être routées vers le service Flask, en utilisant le port 5000.
- **Deployment**: Configure un déploiement Kubernetes pour le serveur Nginx, utilisant l'image `chatodo/nginx:latest`. Ce déploiement crée un réplica de Nginx et expose le serveur sur le port 80.
- **Service**: Établit un service de type `LoadBalancer` pour exposer Nginx à l'extérieur du cluster Kubernetes. Le service écoute sur le port 80 et route le trafic vers le pod Nginx.
### Déploiement
#### Construction de l'image Docker (aussi présent sur DockerHub : chatodo/flask-api)
`docker build -t flask-app:latest .`

#### Déployer sur Kubernetes
```
kubectl apply -f flask/flask.yml
kubectl apply -f nginx/nginx-deployment.yml
```

#### Execution 
`./ingress-forward.sh`
http://localhost:31380/api
On obtient : 
![[12_20.png]]