# 🎙️ Voicelet

<div align="center">

![Voicelet Banner](/cover.png)

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Telegram Bot API](https://img.shields.io/badge/Telegram_Bot_API-v13.7-blue.svg?style=flat&logo=telegram)](https://core.telegram.org/bots/api)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-required-red.svg)](https://ffmpeg.org/)

**A smart Telegram bot that recognizes voice messages with automatic language detection**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Configuration](#configuration) • [Project Structure](#project-structure) • [Author](#author)

</div>

---

## ✨ Features

- 🔊 **Voice Message Recognition** — Convert voice messages to text quickly and accurately
- 🌐 **Automatic Language Detection** — Intelligently identifies the language being spoken
- 🗣️ **Multi-Language Support** — Works with numerous languages including Russian, English, and more
- 🔄 **Audio Processing** — Advanced audio normalization for better recognition quality

## 🚀 Installation

### Prerequisites

- Python 3.11+
- FFmpeg audio processing library
- A Telegram Bot Token (from [@BotFather](https://t.me/BotFather))

### Setup

1. **Clone the repository**

```bash
git clone https://github.com/mirvald-space/voicelet.git
cd voicelet
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Install FFmpeg** (if not already installed)

<details>
<summary>Installation Instructions by OS</summary>

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
Download from [FFmpeg official website](https://ffmpeg.org/download.html)
</details>

4. **Configure environment**

Create a `.env` file in the project root:

```
TELEGRAM_TOKEN=your_telegram_bot_token_here
ENERGY_THRESHOLD=300
LANGUAGES=ru-RU,en-US
```

## 💡 Usage

1. **Start the bot**

```bash
python main.py
```

2. **Interact with your bot on Telegram**

- Send a voice message to your bot
- The bot will respond with the detected language and transcribed text
- Supports multiple languages - just speak naturally!

## ⚙️ Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `TELEGRAM_TOKEN` | Your Telegram bot token from BotFather | *Required* |
| `ENERGY_THRESHOLD` | Sensitivity threshold for speech recognition | 300 |
| `LANGUAGES` | Comma-separated list of language codes to detect | ru-RU,en-US |

## 🗄️ Project Structure

```
.
├── main.py             # Entry point for the bot
├── config.py           # Configuration and settings
├── handlers/           # Message handlers
│   ├── __init__.py     # Handler package initialization
│   └── voice.py        # Voice message handler
├── utils/              # Utility functions
│   ├── __init__.py     # Utils package initialization
│   └── speech.py       # Speech recognition functions
├── .env                # Environment variables file (create this)
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

## 🗣️ Supported Languages

| Language | Code |
|----------|------|
| English  | en-US |
| Russian  | ru-RU |
| French   | fr-FR |
| German   | de-DE |
| Spanish  | es-ES |
| Italian  | it-IT |
| Japanese | ja-JP |

> **Note**: More languages can be added by updating the LANGUAGES parameter in your .env file.


[![GitHub](https://img.shields.io/badge/GitHub-mirvald--space-black?style=flat&logo=github)](https://github.com/mirvald-space)
[![Telegram](https://img.shields.io/badge/Telegram-@your__handle-blue?style=flat&logo=telegram)](https://t.me/voiceletbot)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
<p>If you find this project useful, please consider giving it a ⭐️</p>
<p>Made with ❤️ and Python</p>
</div> 