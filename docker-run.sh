#!/bin/bash

# Скрипт для удобного запуска Telegram бота через Docker

echo "🚀 Запуск Telegram Voice Bot через Docker..."

# Проверяем наличие .env файла
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден!"
    echo "Создайте файл .env с необходимыми переменными окружения"
    exit 1
fi

# Создаем директорию для временных файлов
mkdir -p temp

# Останавливаем существующие контейнеры
echo "🛑 Останавливаем существующие контейнеры..."
docker-compose down

# Собираем и запускаем
echo "🔨 Собираем Docker образ..."
docker-compose build

echo "▶️  Запускаем бота..."
docker-compose up -d

echo "✅ Бот запущен!"
echo "📊 Для просмотра логов: docker-compose logs -f"
echo "🛑 Для остановки: docker-compose down"
echo "🌐 HTTP сервер доступен на: http://localhost:3000"