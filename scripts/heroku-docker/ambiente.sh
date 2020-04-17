export HEROKU_APP=json-reportes-back-heroku
export DOCKER_NOMBRE_IMAGEN=json-reportes-back


# credenciales de Heroku
export HEROKU_EMAIL=${HEROKU_EMAIL:-brian.d.lobo@gmail.com}
export HEROKU_API_KEY=${HEROKU_API_KEY:-a9320074-aa10-4e92-9bf4-2d6818bddd75}
export HEROKU_REGISTRY=registry.heroku.com


# imagen de docker
export DOCKER_NAMESPACE=${DOCKER_NAMESPACE:-brianwolf94}

export CIRCLE_SHA1_SHORT=${CIRCLE_SHA1:0:7}
export DOCKER_TAG=${CIRCLE_SHA1_SHORT:-local}


# forma para que virtualenv no me sustituya algunas variables
export DOLAR=$