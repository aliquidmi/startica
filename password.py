import random, string, logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, MessageHandler, filters
from keyboards import get_main_keyboard

logger = logging.getLogger(name)

REPEAT_BUTTON_TEXT = "Ще раз пароль"

def generate_password() -> str:
    length = random.randint(8, 16)
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    logger.debug(f"Згенерований пароль: {password}")
    return password

def get_password_keyboard():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("Назад"), KeyboardButton(REPEAT_BUTTON_TEXT)]],
        resize_keyboard=True
    )

async def password_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.strip()
        user_id = update.effective_user.id
        logger.info(f"Від {user_id}: {text}")

        if text in ["/password", "🔐 Генератор паролів", REPEAT_BUTTON_TEXT]:
            password = generate_password()
            await update.message.reply_text(
                f"🔐 Ваш випадковий пароль:\n\n`{password}`",
                parse_mode="Markdown", reply_markup=get_password_keyboard()
            )
            logger.info(f"Пароль надіслано користувачу {user_id}")

        elif text == "Назад":
            await update.message.reply_text("Головне меню:", reply_markup=get_main_keyboard())
            logger.info(f"Користувач {user_id} повернувся до меню")

        else:
            await update.message.reply_text("Введіть /password або натисніть кнопку.", reply_markup=get_password_keyboard())
            logger.warning(f"Невідома команда від {user_id}: {text}")

    except Exception as e:
        logger.error(f"❌ Помилка в password_handler: {e}")
        await update.message.reply_text("❌ Сталася помилка при обробці запиту.")

def get_handler():
    return MessageHandler(
        filters.TEXT & filters.Regex(r"^(🔐 Генератор паролів|Ще раз пароль|Назад|/password)$"),
        password_handler
    )