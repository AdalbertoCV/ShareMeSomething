#!/bin/sh

echo "Aplicando migraciones..."
python manage.py migrate

echo "Servidor listo. Ejecutando Django."
exec "$@"