# json-reportes-back

> Servicio para convertir datos en *json* a un template customizable para generar *reportes*, por ahora solo genera pdfs

![alt text](img/reports.gif)

---

## Indice

* [Requerimientos](#requerimientos)
* [Instalacion](#instalacion)
* [Uso](#uso)
* [Dockers](#dockers)
* [Paginas](#paginas)
* [Autor](#autor)

---

## Requerimientos

* Docker instalado

## Instalacion

* Ejecutar desde la raiz del proyecto *(donde esta este readme)* `./sctipts/docker/run.sh`
* Para saber si se levanto de forma ejecutar [0.0.0.0:5000](https://0.0.0.0:5000)

## Uso

* A falta de un front, **solo se puede usar haciendo llamadas rest** desde una herramienta que lo facilite, para ello se deja una **coleccion de Postman** ubicado en: `src/json_reportes.postman_collection.json`

* **Leer las descripciones de las request de Postman** que indican como python toma las variables de los request

* **Se deja como ejemplo** un *template html con css* y un *json de datos* en la ruta `/src/ejemplo_template/`

---

## Dockers

### Construccion para correr localmente

* Ejecutar `./sctipts/docker/build.sh`
* Ejecutar `./sctipts/docker/run.sh`

### Volumes

* **logs**: Logs de la aplicacion, todos los archivos generados tienen extension *.log*
* **archivos**: Sistema de archivos interno de la aplicacion

---

## Paginas

* [Docker Python 3.7 apine](https://hub.docker.com/_/python)

## Autor

> **Brian Lobo**

* Github: [brianwolf](https://github.com/brianwolf)
* Docker Hub:  [brianwolf94](https://hub.docker.com/repository/docker/brianwolf94/json_reportes)
