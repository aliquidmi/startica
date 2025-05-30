from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
from config import BOT_TOKEN
from handlers import calc  # Імпортуємо наш калькулятор
from keyboards import get_main_keyboard  # Імпортуємо клавіатуру

# Стартова команда
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = get_main_keyboard()
    await update.message.reply_text(
        "Привіт! Обери команду з меню:",
        reply_markup=keyboard
    )

# Ініціалізація та запуск бота
def main():
    app = ApplicationBuilder().token("TELEGRAM_BOT_TOKEN").build()

    # Реєстрація обробників команд
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(calc.get_handler())  # /calc

    print("Бот запущено")
    app.run_polling()

if __name__ == "__main__":
    main()
