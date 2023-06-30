#!/bin/bash

# Путь до вашего файла .env
ENV_PATH="./.env"

# Импорт переменных из файла .env
source $ENV_PATH

# Имя файла резервной копии
BACKUP_NAME="db_backup_$(date +'%Y_%m_%d_%H_%M_%S').sql"

# Установка пароля для авторизации в PostgreSQL
export PGPASSWORD=$POSTGRES_PASSWORD

# Команда для создания резервной копии
pg_dump -U $POSTGRES_USER -h $ip -d $DATABASE > $BACKUP_DIR/$BACKUP_NAME

# Обнуление пароля в окружении после использования
unset PGPASSWORD

echo "Backup created at $BACKUP_DIR/$BACKUP_NAME"
