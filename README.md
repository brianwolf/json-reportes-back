# :card_index_dividers: json-reportes-back

> Servicio para convertir datos en *json* a un template customizable para generar *reportes*, por ahora solo genera pdfs y markdown

![alt text](docs/img/reports.gif)

---

## :open_book: Documentacion adicional

* [Instalacion con Docker-Compose](docs/docker-compose.md) *(recomendado)*
* [Instalacion con Docker](docs/docker.md)
* [Instalacion con Python](docs/python.md)

---

## :tada: Uso

* Para ver si todo esta funcionando entrar con el navegador a la url `http://localhost:5000/`, tambien se puede hacer un curl a `http://localhost:5000/vivo`

A falta de un front se deja una **coleccion de Postman** ubicado en: `postman/json_reportes.postman_collection.json`

**Se deja como ejemplo** un *template html con css*, otro con *md* y un *json de datos* en la ruta `/src/ejemplo_template/`

## :scroll: Scripts

Se dejan scripts para facilitar el manejo del proyecto, la cual contiene scripts para docker, heroku, python, etc.
Para ejecutarlos hay que pararse en la ruta raiz del proyecto y llamar el script desde ahi, ejemplo:
`./scripts/docker/build.sh`

## :package: Despliegue

La aplicacion se despliega de forma automatica utilizando *CircleCI* cada vez que se realiza un merge a la rama *master*,
para ello utiliza los scripts dentro de la carpeta `scripts/`, es decir que ejecutar los scripts manualmente es similar a lo que ejecutan las tasks dentro de los jobs del pipeline de circleci

Este despliegue consiste en:

**Docker**:

* Construir una nueva imagen de docker
* Crear un tag para la imagen con la version acortada del commit de *github*
* Subir la imagen a *docker hub*
* Actualizar la version *latest* existente en docker hub a esta ultima

**Heroku**:

* Construir una imagen de docker espificamente para *heroku*
* Subir la imagen creada al registry de heroku
* Desplegar la imagen generada

## :money_with_wings: Heroku

* Ingresar [aqui](https://json-reportes-back-heroku.herokuapp.com/) para probar la aplicacion.
* Al agregarle `/variables` al final de la URL se puede observar la *version* desplegada
  en el atributo del json respuesta `version`

## :earth_americas: Paginas

* [Docker Hub Python](https://hub.docker.com/_/python)
* [CircleCI](https://circleci.com/)
* [Emoticones del Readme](https://github.com/ikatyang/emoji-cheat-sheet)

## :grin: Autor

> **Brian Lobo**

* Github: [brianwolf](https://github.com/brianwolf)
* Docker Hub:  [brianwolf94](https://hub.docker.com/u/brianwolf94)
