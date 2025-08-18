# Makefile для Telegram Voice Bot

.PHONY: help build up down logs restart clean dev

# Показать справку
help:
	@echo "🎙️ Voicelet - Telegram Voice Bot"
	@echo ""
	@echo "Доступные команды:"
	@echo "  build     - Собрать Docker образ"
	@echo "  up        - Запустить бота в фоне"
	@echo "  down      - Остановить бота"
	@echo "  logs      - Показать логи"
	@echo "  restart   - Перезапустить бота"
	@echo "  clean     - Очистить Docker образы и контейнеры"
	@echo "  dev       - Запустить в режиме разработки"

# Собрать образ
build:
	@echo "🔨 Собираем Docker образ..."
	docker-compose build

# Запустить в фоне
up:
	@echo "🚀 Запускаем бота..."
	docker-compose up -d
	@echo "✅ Бот запущен! HTTP сервер: http://localhost:3000"

# Остановить
down:
	@echo "🛑 Останавливаем бота..."
	docker-compose down

# Показать логи
logs:
	@echo "📊 Логи бота:"
	docker-compose logs -f

# Перезапустить
restart: down up

# Очистить всё
clean:
	@echo "🧹 Очищаем Docker..."
	docker-compose down --rmi all --volumes --remove-orphans
	docker system prune -f

# Режим разработки (с автоперезапуском)
dev:
	@echo "🔧 Запуск в режиме разработки..."
	docker-compose up --build