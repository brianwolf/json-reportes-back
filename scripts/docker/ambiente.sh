########################################################
# PUBLICAS
########################################################

export DOCKER_USER=${DOCKER_USER:-brianwolf94}
export DOCKER_TOKEN=${DOCKER_TOKEN:-64f0e37f-eb5a-4072-8b5b-a1a2b7e7b7cf}



########################################################
# PRIVADAS
########################################################

export DOCKER_ARCHIVO_ARGUMENTOS=./config/argumentos.env
export DOCKER_ARCHIVO_AMBIENTE=./config/ambiente.env

export DOCKER_DOCKERFILE=dockerfile

export DOCKER_NOMBRE_IMAGEN=json-reportes-back
export DOCKER_TAG=${CIRCLE_SHA1:-latest}

export DOCKER_NETWORK=docker_red

export DOCKER_PUERTO_INTERNO=5000
export DOCKER_PUERTO_EXTERNO=5000
