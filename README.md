# Bakasur
Distributed Tracking based on Service Mesh 

### Docker Images
    - Service Docker
        - Build: `docker build . -t dt-srv -f serviceDockerfile`
        - Run: `docker run -d -p 8000:8000 dt-srv`

### Push Docker Image to Docker hub
    1.  `docker login -u saintlyzero`
    2.  `docker tag dt-pxy saintlyzero/agni:dt-pxy`
    3.  `docker push saintlyzero/agni:dt-pxy`

### Steps to expose Minikube

    1. `kubectl expose deployment dt-deployment --type=LoadBalancer --port=9000`
    2. `minikube tunnel`
    3. `kubectl get services dt-deployment`


### Handy Commands

Check container logs of all pods
`kubectl logs dt-deployment-86475b7468-dl659 --all-containers -f`
