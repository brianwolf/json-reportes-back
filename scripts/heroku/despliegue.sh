source ./scripts/heroku/ambiente.sh
source ./scripts/docker/ambiente.sh

cd ./scripts/heroku

echo "$HEROKU_API_KEY" | docker login --username $DOCKER_USER --password-stdin registry.heroku.com

heroku create $HEROKU_APP

heroku container:login
heroku container:push web -a $HEROKU_APP --arg TAG=$DOCKER_TAG
heroku container:release web -a $HEROKU_APP

cd ../../
