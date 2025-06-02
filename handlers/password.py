import random
import string
from telegram import Update
from telegram.ext import ContextTypes

# Генерація пароля
def generate_password() -> str:
    length = random.randint(8, 16)
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

# Обробник команди /password
async def password_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        password = generate_password()
        await update.message.reply_text(
            f"🔐 Ось ваш випадковий пароль:\n\n`{password}`",
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text("⚠️ Виникла помилка при генерації пароля.")
        print(f"[ERROR /password]: {e}")