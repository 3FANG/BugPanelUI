#!/bin/sh

# Ждём, пока PostgreSQL не будет готов принимать подключения
# Используем имя сервиса 'postgres' и переменные из .env
echo "Waiting for PostgreSQL to become available..."
until pg_isready -h postgres -p 5432 -U "$DATABASE_USERNAME" -d "$DATABASE_NAME"; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done
echo "PostgreSQL is ready!"

# Применяем миграции
echo "Running alembic upgrade head..."
alembic upgrade head

# Запускаем приложение
echo "Starting Uvicorn..."
exec uvicorn src.main:app --host 0.0.0.0 --port 80