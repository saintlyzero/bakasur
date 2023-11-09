
# Bakasur

Distributed Tracking based on Service Mesh

## Docker

### Docker Images

- Build  & Run
	- Trace Agent Proxy Server
		- Build: `docker build . -t dt-srv -f serviceDockerfile`
		- Run: `docker run -d -p 8000:8000 dt-srv`
	- Trace Collector
		- Build: `docker build . -t dt-c`
		- Run: `docker run -d -p 9001:9001 dt-c`

### Push Docker Image to Docker hub

- Login Registry `docker login -u saintlyzero`

- Build & Push Trace Collector
```sh
docker build . -t dt-c
docker tag dt-c saintlyzero/agni:dt-c
docker push saintlyzero/agni:dt-c
```

- Build & Push Trace Agent Proxy
```sh
docker build . -t dt-pxy -f proxyDockerfile
docker tag dt-pxy saintlyzero/agni:dt-pxy
docker push saintlyzero/agni:dt-pxy
```

- Build & Push Trace Agent Microservice
```sh
cd agent/service-1
docker build . -t dt-srv-1
docker tag dt-srv-1 saintlyzero/agni:dt-srv-1
docker push saintlyzero/agni:dt-srv-1


cd agent/service-2
docker build . -t dt-srv-2
docker tag dt-srv-2 saintlyzero/agni:dt-srv-2
docker push saintlyzero/agni:dt-srv-2
```


### Access K8 Deployments (Minikube) [Not Stable]

- Port Forward
```
kubectl port-forward svc/agent 9000:9000
```
OR
- Expose Deployments
```sh
kubectl expose deployment agent --type=LoadBalancer --port=8000
```
- Get External IP
```sh
kubectl get services
```
- Create Minkube Tunnel (New Termninal)
```sh
minikube tunnel
``` 
kubectl port-forward agent 9000:9000

### Add Load Balancer [Stable]

- Create Minkube Tunnel (New Termninal)
```sh
minikube tunnel
``` 
- Delete existing Service attached to the Deployment
```sh
kubectl delete service <service-name> 
```
- Create a Service of type Load Balancer
```sh
kubectl expose deployment <deployment-name> --type=LoadBalancer --port=<specified-port>
kubectl expose deployment service-1 --type=LoadBalancer --port=9000
```
- Get External IP
```sh
kubectl get services
```

## Database

1. Setup MySQL

```sh
cd database
kubectl apply -f mysql-deployment.yaml
kubectl apply -f mysql-service.yaml
kubectl apply -f mysql-client.yaml
```

2. Access MySQL CLI
```sh
kubectl exec -it mysql-cli-pod -- /bin/sh
mysql -h mysql-service -u root -p -D bakasur
```

3. Connection String from K8s
```python
mysql://root:root@mysql-service:3306/bakasur
```

### Database Schema
```
trace_id, source_id, parent_id, in_time, out_time, status  
```


## Handy Commands

Check container logs of all pods
```sh
kubectl logs <pod-name> --all-containers -f
```


### Fresh Start Steps

```sh
minikube stop
minikube start
kl delete deployment agent, collector
kl delete service agent, collector
kl apply -f agent/deployment.yaml
kl apply -f trace/deployment.yaml
kl port-forward svc/agent 9000:9000
```