docker build . -t dt-pxy -f proxyDockerfile
docker tag dt-pxy saintlyzero/agni:dt-pxy
docker push saintlyzero/agni:dt-pxy