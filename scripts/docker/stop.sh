source ./scripts/docker/ambiente.sh

docker stop $DOCKER_NOMBRE_IMAGEN
docker network rm $DOCKER_NETWORK