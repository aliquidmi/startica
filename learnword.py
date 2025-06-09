import json, random, logging
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ContextTypes, filters
from keyboards import get_main_keyboard, get_learnword_keyboard

logger = logging.getLogger(__name__)

USED_WORDS_FILE = 'used_words.json'
QUIZ_STATE = {}

DEFAULT_WORDS = [
    { "word": "apple", "translation": "яблуко" },
    { "word": "dog", "translation": "собака" },
    { "word": "sun", "translation": "сонце" },
    { "word": "book", "translation": "книга" },
    { "word": "water", "translation": "вода" },
    { "word": "cat", "translation": "кіт" },
    { "word": "tree", "translation": "дерево" },
    { "word": "sky", "translation": "небо" },
    { "word": "house", "translation": "будинок" },
    { "word": "car", "translation": "автомобіль" },
    { "word": "table", "translation": "стіл" },
    { "word": "pen", "translation": "ручка" },
    { "word": "phone", "translation": "телефон" },
    { "word": "milk", "translation": "молоко" },
    { "word": "bread", "translation": "хліб" },
    { "word": "flower", "translation": "квітка" },
    { "word": "mountain", "translation": "гора" },
    { "word": "river", "translation": "річка" },
    { "word": "window", "translation": "вікно" },
    { "word": "door", "translation": "двері" },
    { "word": "chair", "translation": "стілець" },
    { "word": "school", "translation": "школа" },
    { "word": "teacher", "translation": "вчитель" },
    { "word": "student", "translation": "учень" },
    { "word": "music", "translation": "музика" },
    { "word": "game", "translation": "гра" },
    { "word": "fish", "translation": "риба" },
    { "word": "bird", "translation": "птах" },
    { "word": "horse", "translation": "кінь" },
    { "word": "road", "translation": "дорога" },
    { "word": "city", "translation": "місто" },
    { "word": "village", "translation": "село" },
    { "word": "hat", "translation": "капелюх" },
    { "word": "shirt", "translation": "сорочка" },
    { "word": "shoe", "translation": "черевик" },
    { "word": "time", "translation": "час" },
    { "word": "day", "translation": "день" },
    { "word": "night", "translation": "ніч" },
    { "word": "family", "translation": "сім'я" },
    { "word": "friend", "translation": "друг" },
    { "word": "computer", "translation": "комп'ютер" },
    { "word": "work", "translation": "робота" },
    { "word": "money", "translation": "гроші" },
    { "word": "food", "translation": "їжа" },
    { "word": "drink", "translation": "напій" },
    { "word": "air", "translation": "повітря" },
    { "word": "fire", "translation": "вогонь" },
    { "word": "earth", "translation": "земля" },
    { "word": "love", "translation": "любов" },
    { "word": "peace", "translation": "мир" }
]

def load_used_words():
    try:
        with open(USED_WORDS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except Exception as e:
        logger.error(f"Помилка при завантаженні used_words.json: {e}")
        return []

def save_used_words(words):
    try:
        with open(USED_WORDS_FILE, 'w', encoding='utf-8') as f:
            json.dump(words, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(f"Помилка при збереженні used_words.json: {e}")

async def show_random_word(update: Update):
    try:
        used_words = load_used_words()
        remaining = [w for w in DEFAULT_WORDS if w not in used_words]

        if not remaining:
            await update.message.reply_text("✨ Усі слова вже вивчені. Нові незабаром!")
            return

        word_pair = random.choice(remaining)
        used_words.append(word_pair)
        save_used_words(used_words)

        logger.info(f"Нове слово: {word_pair['word']} -> {word_pair['translation']}")
        await update.message.reply_text(
            f"📘 {word_pair['word']} ➡️ {word_pair['translation']}",
            reply_markup=get_learnword_keyboard()
        )
    except Exception as e:
        logger.error(f"Помилка у show_random_word: {e}")
        await update.message.reply_text("❗ Сталася помилка. Спробуйте пізніше.")

async def start_quiz(update: Update):
    try:
        used = load_used_words()
        if not used:
            await update.message.reply_text("⚠️ Немає вивчених слів для перевірки.")
            return

        user_id = update.effective_user.id
        word_pair = random.choice(used)
        QUIZ_STATE[user_id] = word_pair

        logger.info(f"Вікторина для {user_id}: {word_pair['word']}")
        await update.message.reply_text(
            f"🧠 Як перекладається: *{word_pair['word']}*?",
            parse_mode="Markdown",
            reply_markup=get_learnword_keyboard()
        )
    except Exception as e:
        logger.error(f"Помилка у start_quiz: {e}")
        await update.message.reply_text("❗ Помилка при початку вікторини.")

async def handle_quiz_answer(update: Update):
    try:
        user_id = update.effective_user.id
        user_answer = update.message.text.strip().lower()

        correct = QUIZ_STATE[user_id]['translation'].strip().lower()
        word = QUIZ_STATE[user_id]['word']

        if user_answer == correct:
            logger.info(f"Правильно: {word} -> {user_answer}")
            del QUIZ_STATE[user_id]
            await update.message.reply_text(
                f"✅ Правильно! {word} — {correct}",
                reply_markup=get_learnword_keyboard()
            )
        else:
            logger.info(f"Неправильно: {word} -> {user_answer} (правильно: {correct})")
            await update.message.reply_text(
                f"❌ Неправильно. Спробуй ще раз: *{word}*?",
                parse_mode="Markdown",
                reply_markup=get_learnword_keyboard()
            )
    except Exception as e:
        logger.error(f"Помилка у handle_quiz_answer: {e}")
        await update.message.reply_text("❗ Помилка при перевірці відповіді.")

async def learnword_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        logger.info(f"/learnword від {update.effective_user.id}")
        await update.message.reply_text("📚 Вивчай нові слова або перевір свої знання!",
                                        reply_markup=get_learnword_keyboard())
    except Exception as e:
        logger.error(f"Помилка у learnword_command: {e}")

async def learnword_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    logger.info(f"Меню вибір: {text} від {user_id}")
    try:
        if text == "📚 Вивчення слів":
            await learnword_command(update, context)
        elif text == "Нове слово":
            await show_random_word(update)
        elif text == "Перевірити знання":
            await start_quiz(update)
        elif text == "Назад":
            QUIZ_STATE.pop(user_id, None)
            await update.message.reply_text("Головне меню:", reply_markup=get_main_keyboard())
        else:
            await handle_quiz_answer(update)
    except Exception as e:
        logger.error(f"Помилка у learnword_menu_handler: {e}")
        await update.message.reply_text("⚠️ Виникла помилка. Спробуй ще раз.")

def get_handler():
    return [
        CommandHandler("learnword", learnword_command),
        MessageHandler(filters.TEXT & filters.Regex(r"^(📚 Вивчення слів|Нове слово|Перевірити знання|Назад)$"), learnword_menu_handler),
        MessageHandler(filters.TEXT & (~filters.COMMAND), learnword_menu_handler)
    ]