# README pour la Configuration Kubernetes

Le fichier ```myservice.yaml``` est le fichier de configuration.

## Etapes
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
## Explication (celle du tableau)
![Alt text](tableau.png)

## Explication du yaml

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
Ce déploiement crée une instance (*replicas: 1*) du service myservice. 
Il utilise l'image Docker présente sur Dockerhub (*chatodo/myservice:1*) et télécharge l'image si elle n'est pas présente (*imagePullPolicy: IfNotPresent*). 
Le service est configuré pour redémarrer automatiquement en cas de défaillance (*restartPolicy: Always*).

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
Ce service expose le *myservice* sur le port *8080*, et est accessible en dehors du cluster Kubernetes via un *NodePort* sur le port *31280*. 
Le protocole utilisé est TCP.

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
    - microservice-gateway
    http:
    - match:
        - uri:
                prefix: /myservice/ # le gateway va rediriger vers le service myservice
    #        regex: '\/carservice\/*'
        rewrite:
            uri: /
        route:
        - destination:
                port:
                    number: 8080
                host:  myservice.default.svc.cluster.local # DNS qui est démaré par défaut et il s'enregistre avec ce nom
```
Le *VirtualService* définit des règles pour router le trafic vers *myservice*. 
Il redirige les requêtes avec le préfixe */myservice/* vers ce service. 
Toutes les requêtes arrivant à ce chemin sont réécrites pour avoir un URI (Uniform Resource Identifier), ici racine (/), et sont ensuite routées vers le port *8080* de *myservice.default.svc.cluster.local.* Ce DNS est défini par défaut dans Kubernetes.

4. Gateway (Istio)
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
    name: microservice-gateway
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
Le *Gateway* définit un point d'entrée pour le trafic externe. 
Dans ce cas, il écoute sur le port *80* (HTTP) et accepte le trafic de tous les hôtes ("*").
Le sélecteur *istio: ingressgateway* indique qu'il utilise l'*IngressGateway d'Istio*.
