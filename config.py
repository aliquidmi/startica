import os
from dotenv import load_dotenv

# Завантажує .env змінні у середовище
load_dotenv()

# Отримуємо токен
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не знайдено. Перевір .env файл або змінні середовища.")
