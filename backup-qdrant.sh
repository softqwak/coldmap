#!/bin/bash
# backup-qdrant.sh

BACKUP_DIR="/backup/qdrant"
QDRANT_DATA="/opt/qdrant/storage"
DATE=$(date +%Y%m%d_%H%M%S)

# Создание снапшота
docker exec qdrant-storage curl -X POST "http://localhost:6333/collections/my_collection/snapshots"

# Копирование данных
rsync -av --delete $QDRANT_DATA/ $BACKUP_DIR/$DATE/

# Сжатие архива
tar -czf $BACKUP_DIR/qdrant_backup_$DATE.tar.gz -C $BACKUP_DIR $DATE

# Удаление старых бэкапов (старше 7 дней)
find $BACKUP_DIR -name "qdrant_backup_*.tar.gz" -mtime +7 -delete