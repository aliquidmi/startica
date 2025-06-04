import logging
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
from config import BOT_TOKEN

# Імпортуємо обробники
from handlers import calc, translate, password, quote, remind, advice, learnword
from keyboards import get_main_keyboard

# Налаштування логування
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Користувач викликав /start")
    keyboard = get_main_keyboard()
    await update.message.reply_text(
        "Привіт! Обери команду з меню:",
        reply_markup=keyboard
    )

# Глобальний обробник помилок
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Виникла помилка: %s", context.error)
    if isinstance(update, Update) and update.message:
        await update.message.reply_text("Виникла неочікувана помилка. Спробуй пізніше.")

# Запуск бота
def main():
    logger.info("Запуск бота...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Додаємо обробники команд
    app.add_handler(CommandHandler("start", start_command))
    logger.info("Додано обробник /start")

    app.add_handler(calc.get_handler())
    logger.info("Додано обробник /calc")

    app.add_handler(translate.get_handler())
    logger.info("Додано обробник /translate")

    app.add_handler(password.get_handler())
    logger.info("Додано обробник /password")

    app.add_handler(remind.get_handler())
    logger.info("Додано обробник /remind")

    app.add_handler(quote.get_handler())
    logger.info("Додано обробник /quote")

    app.add_handler(advice.get_handler())
    logger.info("Додано обробник /advice")

    app.add_handler(learnword.get_handler())
    logger.info("Додано обробник /learnword")

    # Обробка помилок
    app.add_error_handler(error_handler)
    logger.info("Додано глобальний обробник помилок")

    print("Бот запущено")
    logger.info("Бот запущено")

    app.run_polling()

if __name__ == "__main__":
    main()