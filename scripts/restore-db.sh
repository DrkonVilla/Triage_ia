#!/bin/bash
if [ -z "$1" ]; then
    echo "Uso: ./restore-db.sh <archivo_backup.sql>"
    exit 1
fi
docker exec -i triage-postgres psql -U triaje_user -d triaje_db < "$1"
echo "✅ Restauración completada"