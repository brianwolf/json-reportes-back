source ./scripts/docker/ambiente.sh

docker logs \
$DOCKER_NOMBRE_IMAGEN \
-f
