from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters
from deep_translator import GoogleTranslator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGES = {
    'en': 'english',
    'fr': 'french',
    'de': 'german',
    'uk': 'ukrainian',
}

HELP_MESSAGE = (
    "🌍 Введи команду для перекладу у форматі:\n"
    "<code>/translate &lt;мова&gt; &lt;текст&gt;</code>\n\n"
    "Або просто напиши повідомлення типу:\n"
    "<code>en Привіт</code>\n\n"
    "Підтримувані мови: en, fr, de, uk"
)

async def translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 2:
            raise ValueError("Недостатньо аргументів.")
        lang, text = args[0].lower(), ' '.join(args[1:])
        await handle_translation(update, lang, text)
    except Exception as e:
        logger.exception(f"Помилка в translate_command: {e}")
        await update.message.reply_text(HELP_MESSAGE, parse_mode="HTML")

async def text_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.strip()
        parts = text.split(maxsplit=1)
        if len(parts) < 2:
            raise ValueError("Недостатньо слів для перекладу.")
        lang, text_to_translate = parts[0].lower(), parts[1]
        await handle_translation(update, lang, text_to_translate)
    except Exception as e:
        logger.exception(f"Помилка в text_message_handler: {e}")
        await update.message.reply_text("⚠️ Недостатньо інформації або неправильний формат.\n\n" + HELP_MESSAGE, parse_mode="HTML")

async def handle_translation(update: Update, lang: str, text: str):
    try:
        if lang not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Невідома мова: {lang}")

        if not text.strip():
            raise ValueError("Порожній текст для перекладу.")

        translator = GoogleTranslator(source='auto', target=lang)
        translated_text = translator.translate(text)
        logger.info(f"Перекладено: '{text}' -> '{translated_text}' [{lang}]")
        await update.message.reply_text(f"🌍 <b>Переклад:</b>\n{translated_text}", parse_mode="HTML")

    except ValueError as ve:
        logger.warning(f"Помилка валідації: {ve}")
        await update.message.reply_text(f"❌ {ve}\n\n{HELP_MESSAGE}", parse_mode="HTML")

    except Exception as e:
        logger.exception(f"Помилка при перекладі: {e}")
        await update.message.reply_text("❗ Сталася помилка під час перекладу. Спробуй пізніше.")

async def translate_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(HELP_MESSAGE, parse_mode="HTML")
    except Exception as e:
        logger.exception(f"Помилка при відправці HELP_MESSAGE: {e}")

def get_handler():
    lang_pattern = '|'.join(SUPPORTED_LANGUAGES.keys())
    return [
        CommandHandler("translate", translate_command),
        MessageHandler(filters.TEXT & filters.Regex(r'^🌍 Перекладач$'), translate_button_handler),
        MessageHandler(filters.TEXT & filters.Regex(rf'^({lang_pattern})\s+'), text_message_handler),
    ]
