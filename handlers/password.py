import random
import string
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
import logging
from keyboards import get_navigation_keyboard, get_main_keyboard

# Ініціалізуємо лог
logger = logging.getLogger(name)

# Генерація пароля
def generate_password() -> str:
    length = random.randint(8, 16)
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

# Обробник команди /password
async def password_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        text = update.message.text

        if text == "/password" or text == "Ще раз":
            password = generate_password()
            keyboard = get_navigation_keyboard()
            await update.message.reply_text(
                f"Ось ваш випадковий пароль:\n\n`{password}`",
                parse_mode="Markdown"
            )
            logger.info("Пароль згенеровано і надіслано користувачу.")

        elif text == "Назад":
            keyboard = get_main_keyboard()
            await update.message.reply_text("Повернулись у головне меню.", reply_markup=keyboard)
            logger.info(f"Користувач повернувся у головне меню.")

        else:
            await update.message.reply_text(
                "Введи /password або натисни кнопку.",
                reply_markup=get_navigation_keyboard()
            )
            logger.warning(f"Користувач надіслав невідому команду: {text}")

    except Exception as e:
        logger.error(f"Помилка в password_handler: {e}")
        await update.message.reply_text("Виникла помилка при генерації пароля.")