# Heroku

> Permite subir una imagen Docker a Heroku

## Requerimientos

* Archivo `Dockerfile` con ese mismo nombre ubicado en esta misma carpeta que Heroku usara para el despliegue

## Uso

* Ejecutar el script llamado `despliegue.sh`

## Generacion del archivo Dockerfile

En caso de querer generar un archivo de forma dinamica se puede hacer mediante un template
siguiendo estos pasos:

* Crear un archivo llamado `Dockerfile.template` como en el ejemplo
* Ejecutar el script llamado `generar-dockerfile.sh`
* Ejecutar el script llamado `despliegue.sh`

## Importante

Heroku usa una variable de ambiente llamada **$PORT** que tiene el puerto asignado por el server, es **crucial que se utilice en el dockerfile**
