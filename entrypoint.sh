#!/bin/sh
# Comando para esperar que el contenedor de PostgresQL este arriba
echo "Esperando a que PostgreSQL esté disponible..."
/usr/local/bin/wait-for postgres:5432 -- echo "PostgreSQL is up - executing command"
echo "Iniciando servidor Django..."
exec "$@"
