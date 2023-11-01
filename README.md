
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
docker build . -t dt-srv -f serviceDockerfile
docker tag dt-srv saintlyzero/agni:dt-srv
docker push saintlyzero/agni:dt-srv
```


### Access K8 Deployments (Minikube)


- Expose Deployments
```sh
kubectl expose deployment deployment-c --type=LoadBalancer --port=9001
kubectl expose deployment dt-deployment --type=LoadBalancer --port=9000
```
- Get External IP
```sh
kubectl get services
```
- Create Minkube Tunnel (New Termninal)
```sh
minikube tunnel
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
mysql -h mysql-service -u root -p
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
kubectl logs <deployment-name> --all-containers -f
```

