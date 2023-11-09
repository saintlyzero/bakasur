# todo: add args parsing

# kn dt
kubectl apply -f collector/deployment.yaml
kubectl apply -f agent/service-1/deployment.yaml
kubectl apply -f agent/service-2/deployment.yaml
kubectl apply -f agent/service-3/deployment.yaml
kubectl apply -f agent/service-4/deployment.yaml
kubectl apply -f agent/service-5/deployment.yaml
kubectl apply -f agent/service-6/deployment.yaml
kubectl apply -f agent/service-7/deployment.yaml


# delete
# kubectl delete deployment service-1 service-2 service-3 service-4 service-5 service-6 service-7
# kubectl delete service service-1 service-2 service-3 service-4 service-5 service-6 service-7

