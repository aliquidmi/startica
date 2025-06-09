from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from deep_translator import GoogleTranslator
import logging

# Ініціалізація логування
logging.basicConfig(level=logging.INFO)

# Список мов
SUPPORTED_LANGUAGES = {
    'en': 'english',
    'fr': 'french',
    'de': 'german',
    'uk': 'ukrainian',
}

async def translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if len(args) < 2:
        await update.message.reply_text("️ Формат: /translate <мова> <текст для перекладу>")
        return

    lang = args[0].lower()
    text = ' '.join(args[1:])

    if lang not in SUPPORTED_LANGUAGES:
        await update.message.reply_text(f" Невідома мова: '{lang}'. Спробуй, наприклад: en, fr, de, uk")
        return

    try:
        translator = GoogleTranslator(source='auto', target=lang)
        translated_text = translator.translate(text)
        await update.message.reply_text(f" Переклад: {translated_text}")
    except Exception as e:
        logging.error(f"Помилка перекладу: {e}")
        await update.message.reply_text(" Сталася помилка під час перекладу. Спробуй пізніше.")

def get_handler():
    return CommandHandler("translate", translate_command)
