FROM python:3.8.3-slim

ARG ARG_VERSION=local

WORKDIR /usr/src/


# VARIABLES PREDEFINIDAS
ENV VERSION=${ARG_VERSION}

ENV PYTHON_HOST=0.0.0.0
ENV PYTHON_PORT=5000
ENV PYTHON_GUNICORN_WORKERS=1
ENV PYTHON_GUNICORN_CONNECTIONS=1000


# EJECUCION
CMD gunicorn \
    -b ${PYTHON_HOST}:${PYTHON_PORT} \
    --reload \
    --workers=${PYTHON_GUNICORN_WORKERS} \
    --worker-connections=${PYTHON_GUNICORN_CONNECTIONS} \
    app:app

EXPOSE ${PYTHON_PORT}


# WKHTMLTOPDF
RUN apt-get update
RUN apt-get install wkhtmltopdf -y


# DEPENDENCIAS
RUN pip install compile --upgrade pip

COPY ./src/requirements.txt .
RUN pip install -r requirements.txt
RUN rm requirements.txt


# RECURSOS
COPY ./src/consume ./consume


# COMPILACION
COPY ./src/apps ./src/apps
COPY ./src/app.py ./src

RUN python -m compile -b -f -o ./dist ./src
RUN mv -f ./dist/src/* .
RUN rm -fr ./src ./dist