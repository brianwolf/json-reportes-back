. ./scripts/docker/ambiente.sh

echo "$DOCKER_TOKEN" | docker login $DOCKER_REGISTRY --username $DOCKER_USER --password-stdin

printf "\n\nSubiendo imagen con TAG:$VERSION\n"
docker push $DOCKER_REGISTRY/$DOCKER_NAMESPACE/$DOCKER_NOMBRE_IMAGEN:$VERSION

docker tag \
$DOCKER_REGISTRY/$DOCKER_NAMESPACE/$DOCKER_NOMBRE_IMAGEN:$VERSION \
$DOCKER_REGISTRY/$DOCKER_NAMESPACE/$DOCKER_NOMBRE_IMAGEN:latest

printf "\n\nSubiendo imagen con TAG:latest\n"
docker push $DOCKER_REGISTRY/$DOCKER_NAMESPACE/$DOCKER_NOMBRE_IMAGEN:latest