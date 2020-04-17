. ./scripts/heroku-docker/ambiente.sh


DOCKERFILE_HEROKU_FINAL=./scripts/heroku-docker/Dockerfile

envsubst < $DOCKERFILE_HEROKU_FINAL.template > $DOCKERFILE_HEROKU_FINAL

printf "DOCKERFILE GENERADO: \n\n"
cat $DOCKERFILE_HEROKU_FINAL
printf "\n\n"
