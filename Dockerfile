# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем системные зависимости для аудио обработки
RUN apt-get update && apt-get install -y \
    ffmpeg \
    portaudio19-dev \
    python3-pyaudio \
    flac \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Открываем порт для HTTP сервера
EXPOSE 3000

# Команда запуска
CMD ["python", "main.py"]