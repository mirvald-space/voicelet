# 🎙️ Voicelet

<div align="center">

![Voicelet Banner](/cover.png)

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Telegram Bot API](https://img.shields.io/badge/Telegram_Bot_API-v13.7-blue.svg?style=flat&logo=telegram)](https://core.telegram.org/bots/api)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-required-red.svg)](https://ffmpeg.org/)

**Розумний Telegram-бот, який розпізнає голосові повідомлення з автоматичним визначенням мови**

[Можливості](#можливості) • [Встановлення](#встановлення) • [Використання](#використання) • [Конфігурація](#конфігурація) • [Структура проекту](#структура-проекту) • [Автор](#автор)

</div>

---

## ✨ Можливості

- 🔊 **Розпізнавання голосових повідомлень** — Швидко та точно перетворює голосові повідомлення на текст
- 🌐 **Автоматичне визначення мови** — Інтелектуально визначає мову мовлення
- 🗣️ **Багатомовна підтримка** — Працює з багатьма мовами, включаючи українську, англійську та інші
- 🔄 **Обробка аудіо** — Покращена нормалізація аудіо для кращої якості розпізнавання

## 🚀 Встановлення

### Необхідне

- Python 3.11+
- Бібліотека для обробки аудіо FFmpeg
- Токен Telegram-бота (отримати у [@BotFather](https://t.me/BotFather))

### Налаштування

1. **Клонувати репозиторій**

```bash
git clone https://github.com/mirvald-space/voicelet.git
cd voicelet
```

2. **Встановити залежності**

```bash
pip install -r requirements.txt
```

3. **Встановити FFmpeg** (якщо ще не встановлено)

<details>
<summary>Інструкції для різних ОС</summary>

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
Завантажити з [офіційного сайту FFmpeg](https://ffmpeg.org/download.html)
</details>

4. **Налаштувати середовище**

Створіть файл `.env` у корені проекту:

```
TELEGRAM_TOKEN=your_telegram_bot_token_here
ENERGY_THRESHOLD=300
LANGUAGES=ru-RU,en-US
```

## 💡 Використання

1. **Запустіть бота**

```bash
python main.py
```

2. **Взаємодійте з ботом у Telegram**

- Надішліть голосове повідомлення боту
- Бот відповість визначеною мовою та розшифрованим текстом
- Підтримка декількох мов — просто говоріть природно!

## ⚙️ Конфігурація

| Параметр | Опис | Значення за замовчуванням |
|----------|------|--------------------------|
| `TELEGRAM_TOKEN` | Токен Telegram-бота від BotFather | *Обов'язково* |
| `ENERGY_THRESHOLD` | Поріг чутливості для розпізнавання мови | 300 |
| `LANGUAGES` | Список мов через кому для розпізнавання | ru-RU,en-US |

## 🗄️ Структура проекту

```
.
├── main.py             # Точка входу для бота
├── config.py           # Конфігурація та налаштування
├── handlers/           # Обробники повідомлень
│   ├── __init__.py     # Ініціалізація пакету обробників
│   └── voice.py        # Обробник голосових повідомлень
├── utils/              # Утиліти
│   ├── __init__.py     # Ініціалізація пакету утиліт
│   └── speech.py       # Функції розпізнавання мови
├── .env                # Файл змінних середовища (створіть його)
├── .gitignore          # Правила ігнорування Git
└── README.md           # Документація проекту
```

## 🗣️ Підтримувані мови

| Мова      | Код   |
|-----------|-------|
| Англійська | en-US |
| Російська  | ru-RU |
| Французька | fr-FR |
| Німецька   | de-DE |
| Іспанська  | es-ES |
| Італійська | it-IT |
| Японська   | ja-JP |

> **Примітка**: Можна додати більше мов, оновивши параметр LANGUAGES у файлі .env.

[![GitHub](https://img.shields.io/badge/GitHub-mirvald--space-black?style=flat&logo=github)](https://github.com/mirvald-space)
[![Telegram](https://img.shields.io/badge/Telegram-@your__handle-blue?style=flat&logo=telegram)](https://t.me/voiceletbot)

## 📜 Ліцензія

Цей проект ліцензовано за MIT License — див. файл [LICENSE](LICENSE) для деталей.

---

<div align="center">
<p>Якщо проект був корисним, будь ласка, поставте ⭐️</p>
<p>Зроблено з ❤️ та Python</p>
</div> 