#!/bin/bash
BACKUP_DIR="./backups"
mkdir -p $BACKUP_DIR
DATE=$(date +%Y%m%d_%H%M%S)
docker exec triage-postgres pg_dump -U triaje_user triaje_db > "$BACKUP_DIR/backup_$DATE.sql"
echo "✅ Backup guardado en $BACKUP_DIR/backup_$DATE.sql"