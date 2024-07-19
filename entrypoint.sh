#!/bin/sh
echo "Esperando a que PostgreSQL esté disponible..."
# Espera a que PostgreSQL esté disponible
/usr/local/bin/wait-for postgres:5432 -- echo "PostgreSQL is up - executing command"
echo "Iniciando servidor Django..."
# Ejecuta el comando dado (por defecto: iniciar el servidor)
exec "$@"
