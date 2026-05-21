#!/bin/bash

# Limpiar contenedores y carpetas previas para evitar errores de duplicado
docker stop samplerunning || true
docker rm samplerunning || true
rm -rf tempdir

mkdir tempdir
mkdir tempdir/templates
mkdir tempdir/static

cp sample_app.py tempdir/.
cp -r templates/* tempdir/templates/.
cp -r static/* tempdir/static/.

# USAMOS ">" EN EL PRIMERO PARA AGREGAR DE CERO Y LA VERSIÓN SLIM QUE SÍ FUNCIONA
echo "FROM python:3.9-slim" > tempdir/Dockerfile
echo "RUN pip install --no-cache-dir flask" >> tempdir/Dockerfile
echo "COPY  ./static /home/myapp/static/" >> tempdir/Dockerfile
echo "COPY  ./templates /home/myapp/templates/" >> tempdir/templates/" >> tempdir/Dockerfile
echo "COPY  sample_app.py /home/myapp/" >> tempdir/Dockerfile
echo "EXPOSE 6789" >> tempdir/Dockerfile
echo "CMD python3 /home/myapp/sample_app.py" >> tempdir/Dockerfile

cd tempdir
docker build -t sampleapp .
docker run -t -d -p 6789:6789 --privileged --name samplerunning sampleapp
docker ps -a
