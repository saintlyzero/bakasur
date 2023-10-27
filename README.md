
# Bakasur

Distributed Tracking based on Service Mesh

### Docker Images

- Build  & Run
	- Build: `docker build . -t dt-srv -f serviceDockerfile`
	- Run: `docker run -d -p 8000:8000 dt-srv`

### Push Docker Image to Docker hub

 1. Login Registry `docker login -u saintlyzero`
 2. Tag Docker Images `docker tag dt-pxy saintlyzero/agni:dt-pxy`
 3. Push Image to Registry `docker push saintlyzero/agni:dt-pxy`

### Expose Minikube

1. Expose Deployment `kubectl expose deployment dt-deployment --type=LoadBalancer --port=9000`
2. Create Tunnel `minikube tunnel`
3. Get External IP `kubectl get services dt-deployment`
  
### Handy Commands

Check container logs of all pods
`kubectl logs <deployment-name> --all-containers -f`