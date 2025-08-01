# 🎙️ Voicelet

<div align="center">

![Voicelet Banner](/cover.png)

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Telegram Bot API](https://img.shields.io/badge/Telegram_Bot_API-v13.7-blue.svg?style=flat&logo=telegram)](https://core.telegram.org/bots/api)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-required-red.svg)](https://ffmpeg.org/)

**Умный Telegram-бот, который распознаёт голосовые сообщения с автоматическим определением языка**

[Возможности](#возможности) • [Установка](#установка) • [Использование](#использование) • [Конфигурация](#конфигурация) • [Структура проекта](#структура-проекта) • [Автор](#автор)

</div>

---

## ✨ Возможности

- 🔊 **Распознавание голосовых сообщений** — Быстро и точно преобразует голосовые сообщения в текст
- 🌐 **Автоматическое определение языка** — Интеллектуально определяет язык речи
- 🗣️ **Мультиязычная поддержка** — Работает с разными языками, включая русский, английский и другие
- 🔄 **Обработка аудио** — Продвинутая нормализация аудио для лучшего качества распознавания

## 🚀 Установка

### Необходимое ПО

- Python 3.11+
- Библиотека для обработки аудио FFmpeg
- Токен Telegram-бота (получить у [@BotFather](https://t.me/BotFather))

### Установка

1. **Клонируйте репозиторий**

```bash
git clone https://github.com/mirvald-space/voicelet.git
cd voicelet
```

2. **Установите зависимости**

```bash
pip install -r requirements.txt
```

3. **Установите FFmpeg** (если ещё не установлен)

<details>
<summary>Инструкции по установке для разных ОС</summary>

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**  
Скачайте с [официального сайта FFmpeg](https://ffmpeg.org/download.html)
</details>

4. **Настройте окружение**

Создайте файл `.env` в корне проекта:

```
TELEGRAM_TOKEN=your_telegram_bot_token_here
ENERGY_THRESHOLD=300
LANGUAGES=ru-RU,en-US
```

## 💡 Использование

1. **Запустите бота**

```bash
python main.py
```

2. **Взаимодействуйте с ботом в Telegram**

- Отправьте голосовое сообщение боту
- Бот ответит с определённым языком и расшифрованным текстом
- Поддержка нескольких языков — просто говорите естественно!

## ⚙️ Конфигурация

| Параметр | Описание | Значение по умолчанию |
|----------|----------|----------------------|
| `TELEGRAM_TOKEN` | Токен Telegram-бота от BotFather | *Обязателен* |
| `ENERGY_THRESHOLD` | Порог чувствительности для распознавания речи | 300 |
| `LANGUAGES` | Список языков через запятую для распознавания | ru-RU,en-US |

## 🗄️ Структура проекта

```
.
├── main.py             # Точка входа для бота
├── config.py           # Конфигурация и настройки
├── handlers/           # Обработчики сообщений
│   ├── __init__.py     # Инициализация пакета обработчиков
│   └── voice.py        # Обработчик голосовых сообщений
├── utils/              # Утилиты
│   ├── __init__.py     # Инициализация пакета утилит
│   └── speech.py       # Функции распознавания речи
├── .env                # Файл переменных окружения (создайте его)
├── .gitignore          # Правила игнорирования Git
└── README.md           # Документация проекта
```

## 🗣️ Поддерживаемые языки

| Язык    | Код   |
|---------|-------|
| Английский | en-US |
| Русский    | ru-RU |
| Французский| fr-FR |
| Немецкий   | de-DE |
| Испанский  | es-ES |
| Итальянский| it-IT |
| Японский   | ja-JP |

> **Примечание**: Можно добавить больше языков, обновив параметр LANGUAGES в файле .env.

[![GitHub](https://img.shields.io/badge/GitHub-mirvald--space-black?style=flat&logo=github)](https://github.com/mirvald-space)
[![Telegram](https://img.shields.io/badge/Telegram-@your__handle-blue?style=flat&logo=telegram)](https://t.me/voiceletbot)

## 📜 Лицензия

Этот проект распространяется по лицензии MIT — см. файл [LICENSE](LICENSE) для подробностей.

---

<div align="center">
<p>Если проект оказался полезен, пожалуйста, поставьте ⭐️</p>
<p>Сделано с ❤️ и на Python</p>
</div> 