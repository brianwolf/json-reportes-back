source ./scripts/heroku/ambiente.sh
source ./scripts/docker/ambiente.sh


DOCKERFILE_HEROKU_FINAL=./scripts/heroku/Dockerfile


# GENERAR BASE DEL ARCHIVO CON EL "FROM"
envsubst < ./scripts/heroku/templates/from.temp.dockerfile > $DOCKERFILE_HEROKU_FINAL


# SE CARGAN LAS VARIABLES DE AMBIENTE
for i in `cat $DOCKER_ARCHIVO_AMBIENTE`; 
do
    printf "ENV $i\n" >> $DOCKERFILE_HEROKU_FINAL
done


# SE AGREGA EL COMANDO "CMD"
cat ./scripts/heroku/templates/cmd.temp.dockerfile >> $DOCKERFILE_HEROKU_FINAL


# SE MUESTRA EL RESULTADO
printf "DOCKERFILE GENERADO: \n\n"
cat $DOCKERFILE_HEROKU_FINAL