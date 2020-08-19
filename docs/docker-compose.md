# :whale: Instalacion con Docker-compose

> El **docker-compose.yml** se encuentra en la carpeta **docker**

![alt text](img/docker-compose.svg)

## Correr la imagen local

* Ejecutar el script: `./sctipts/compose/up.sh`

Para parar la imagen ejecutar el script: `./sctipts/compose/down.sh`
Los scripts solo ejecutan *docker-compose -f <docker-compose.yml>*

## Puertos

* **5000**: api web de la aplicación

## Volumes

* **json-reportes-back/produces**: Contiene los archivos generados por la aplicacion

---

[Volver al readme principal](../README.md)
