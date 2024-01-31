<div id="user-content-toc">
    <ul>
        <li><a href="#publish-the-image-to-the-docker-hub">1. Publish the image to the Docker Hub</a> </li>
        <li><a href="#kubernetes-deployment">2. Kubernetes deployment</a></li>
        <li><a href="#servicemesh"> 3. Servicemesh </li>
        <li><a href="#monitoring"> 3.1 Monitoring (Kiali/Graphana) </li>
        <li><a href="#frontend-backend-with-kubernetes"> 4. Frontend/Backend With Kubernetes </li>
    </ul>
</div>

## Publish the image to the Docker Hub
[Source](https://github.com/charroux/kubernetes-minikube?tab=readme-ov-file#publish-the-image-to-the-docker-hub)

Build the docker images: ```docker build -t NAME .```

Retreive the image ID: ```docker images```

Tag the docker image: ```docker tag imageID yourDockerHubName/imageName:version```

Example: ```docker tag 900250cf7694 chatodo/NAME:1```

Login to docker hub:

```docker login -u yourDockerHubName --password-stdin```

Push the image to the docker hub: ```docker push yourDockerHubName/imageName:version```

```docker push chatodo/myservice:1``` ou ```docker push chatodo/myservice:latest```

## Kubernetes deployment
Fichier : `myservice-deployment.yml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myservice
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myservice
  template:
    metadata:
      labels:
        app: myservice
    spec:
      containers:
        - image: chatodo/myservice:1
          imagePullPolicy: IfNotPresent
          name: myservice
      restartPolicy: Always
```
- `apiVersion`: Spécifie la version de l'API de Kubernetes utilisée pour créer cet objet
- `kind`: Type de l'objet Kubernetes que ce fichier décrit (ici Deployment)
- `replicas`: Nombre de répliques du Pod à maintenir
- `matchLabels`: Les labels utilisés pour faire correspondre les Pods
- `image`: Nom de l'image Docker à utiliser pour le conteneur
- `imagePullPolicy`: Politique de téléchargement de l'image. *IfNotPresent* signifie que l'image sera téléchargée uniquement si elle n'est pas déjà présente localement
- `restartPolicy`: Politique de redémarrage des conteneurs du Pod. *Always* signifie que le conteneur sera redémarré automatiquement en cas de défaillance
## Servicemesh
### Etapes
1. Démarrage de Minikube avec Docker :
```
minikube start --cpus=2 --memory=5000 --driver=docker
```
2. Appliquer la configuration Kubernetes :
```
kubectl apply -f myservice.yaml
```
3. Configurer l'ingress, soit via le script :
```
./ingress-forward.sh
```
Ou directement avec kubectl :
```
kubectl -n istio-system port-forward deployment/istio-ingressgateway 31380:8080
```
4. Accéder au service via :

```
http://localhost:31380/myservice/
```
---
### Explication (celle du tableau)
![Explication](tableau.png)

### Explication du yaml
Fichier ```myservice.yml```
1. Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
    name: myservice
spec:
    replicas: 1
    selector:
        matchLabels:
            app: myservice
    template:
        metadata:
            labels:
                app: myservice
        spec:
            containers:
                - image: chatodo/myservice:1
                    imagePullPolicy: IfNotPresent
                    name: myservice
            restartPolicy: Always
```
2. Service
```yaml
apiVersion: v1
kind: Service
metadata:
    name: myservice
spec:
    ports:
        - nodePort: 31280
            port: 8080
            protocol: TCP
            targetPort: 8080
    selector:
        app: myservice
    type: NodePort
```
- `nodePort`: Spécifie le port sur lequel le service sera exposé à l'extérieur du cluster Kubernetes. Ici, le nodePort est 31280, ce qui signifie que le service sera accessible via ce port sur l'adresse IP de n'importe quel nœud du cluster
- `port`: Le port interne du cluster sur lequel le service est exposé. Dans ce cas, 8080 est le port sur lequel le service est exposé à l'intérieur du cluster
- `targetPort`: Le port sur lequel le Pod cible est à l'écoute. Cela permet au service de router le trafic vers le bon port au sein du Pod
- `selector.app`:  Route le trafic vers les Pods qui correspondent aux labels spécifiés ici
- `type`: Indique le type de service (NodePort est un type qui expose le service sur un port statique sur chaque nœud du cluster)

3. VirtualService (Istio)
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
    name: myservice
spec:
    hosts:
    - "*"
    gateways:
    - gateway
    http:
    - match:
        - uri:
                prefix: /myservice/ 
        rewrite:
            uri: /
        route:
        - destination:
                port:
                    number: 8080
                host:  myservice.default.svc.cluster.local
```
- `hosts`: Définit les hôtes pour lesquels les règles de routage s'appliquent. `*` indique que les règles s'appliqueront à tous les hôtes
- `gateways`: Référence aux *gateways Istio* qui sont utilisées pour gérer l'entrée du trafic. Ici, *microservice-gateway* est le nom de la gateway définie plus loin dans la configuration
- `match.uri.prefix`: Spécifie le chemin d'accès utilisé pour faire correspondre les requêtes entrantes
- `rewrite.uri`: Le chemin est écrit en /, ce qui signifie que le préfixe */myservice/* est supprimé du chemin de la requête --> fin adresse service
- `route.destination`: Indique la destination du trafic après application des règles de routage et de réécriture. Ici, le trafic est dirigé vers le port *8080* du service *myservice.default.svc.cluster.local*

4. Gateway (Istio)
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
    name: gateway
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
- `istio: ingressgateway`: Cela signifie que cette configuration de Gateway s'appliquera aux pods d'Ingress Gateway d'Istio qui ont le label *istio=ingressgateway*
- `hosts`: Spécifie les hôtes qui sont autorisés à passer par cette Gateway. `*` signifie que la Gateway acceptera le trafic pour tous les domaines.

### Monitoring

#### Kiali dashboard
Kiali est une console pour le service mesh Istio, offrant une visualisation et une gestion des microservices dans le réseau Istio.
Kiali fournit une vue d'ensemble des services et des flux de trafic, facilitant ainsi le débogage et la compréhension de la structure de l'application.

```
kubectl -n istio-system port-forward deployment/kiali 20001:20001
```
Accès à Kiali : <http://localhost:20001>

#### Graphana
Il est utilisé ici pour observer les métriques collectées par Istio, permettant une analyse approfondie de la performance des services.
```
kubectl -n istio-system port-forward deployment/grafana 3000:3000
```
Accès à Grafana : <http://localhost:3000/>

## Frontend Backend With Kubernetes

Fichier : `front-back-app.yml`

```kubectl apply -f front-back-app.yml```

<http://localhost:31380/frontend/>