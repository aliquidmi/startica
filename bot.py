import logging, asyncio, sys, nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
import quote, learnword, remind, advice, calc, translate, password
from config import BOT_TOKEN
from keyboards import get_main_keyboard

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Користувач викликав /start")
    keyboard = get_main_keyboard()
    await update.message.reply_text(
        "🌿 Привіт! Обери команду з меню:",
        reply_markup=keyboard
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Виникла помилка: %s", context.error)
    if isinstance(update, Update) and update.message:
        await update.message.reply_text("Виникла неочікувана помилка. Спробуй пізніше.")

async def main():
    logger.info("Запуск бота...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(calc.get_handler())
    app.add_handler(password.get_handler())

    for handler in remind.get_handler():
        app.add_handler(handler)

    for handler in quote.get_handler():
        app.add_handler(handler)

    for handler in advice.get_handler():
        app.add_handler(handler)

    for handler in translate.get_handler():
        app.add_handler(handler)

    for handler in learnword.get_handler():
        app.add_handler(handler)

    app.add_error_handler(error_handler)

    remind.start_scheduler()

    await app.run_polling()


if __name__ == "__main__":
    if sys.platform.startswith('win') and sys.version_info >= (3, 8):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    nest_asyncio.apply()

    asyncio.run(main())
