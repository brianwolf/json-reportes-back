. ./scripts/docker/ambiente.sh

docker build \
--build-arg ARG_VERSION=$VERSION \
$(for i in `cat $DOCKER_ARCHIVO_ARGUMENTOS`; do out+="--build-arg $i " ; done; echo $out;out="") \
-f $DOCKER_DOCKERFILE \
-t $DOCKER_NAMESPACE/$DOCKER_NOMBRE_IMAGEN:$VERSION .