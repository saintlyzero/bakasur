echo "Building Docker Image"

docker build . -t dt-srv -f serviceDockerfile
docker build . -t dt-pxy -f proxyDockerfile
echo
echo "Build complete ✅"

echo "Starting Service Container"
docker run -d -p 8000:8000 dt-srv

echo "Starting Proxy Container"
docker run -d -p 9000:9000 dt-pxy

echo
echo "Success 🏁"


