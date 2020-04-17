. ./scripts/docker/ambiente.sh

docker network create $DOCKER_NETWORK

docker run -d --rm \
--network $DOCKER_NETWORK \
--env-file $DOCKER_ARCHIVO_AMBIENTE \
--name $DOCKER_NOMBRE_IMAGEN \
-p $DOCKER_PUERTO_EXTERNO:$DOCKER_PUERTO_INTERNO \
$DOCKER_USER/$DOCKER_NOMBRE_IMAGEN:$DOCKER_TAG
