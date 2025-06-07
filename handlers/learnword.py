import os
import json
import random
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ContextTypes, filters
from keyboards import get_main_keyboard, get_learnword_keyboard

WORDS_FILE = 'words.json'

def create_words_file():
    if not os.path.exists(WORDS_FILE):
        default_words = [
            {"word": "apple", "translation": "яблуко"},
            {"word": "dog", "translation": "собака"},
            {"word": "sun", "translation": "сонце"},
            {"word": "book", "translation": "книга"},
            {"word": "water", "translation": "вода"}
        ]
        with open(WORDS_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_words, f, ensure_ascii=False, indent=4)

async def send_random_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open(WORDS_FILE, 'r', encoding='utf-8') as f:
            words = json.load(f)

        if not words:
            await update.message.reply_text("️ Список слів порожній.")
            return

        word_pair = random.choice(words)
        word = word_pair.get("word")
        translation = word_pair.get("translation")

        if not word or not translation:
            await update.message.reply_text("️ Неправильний формат слова.")
            return

        message = f" {word} /  {translation}"
        await update.message.reply_text(message, reply_markup=get_learnword_keyboard())

    except FileNotFoundError:
        await update.message.reply_text(" Файл words.json не знайдено.")
    except json.JSONDecodeError:
        await update.message.reply_text(" Помилка у форматі JSON.")
    except Exception as e:
        await update.message.reply_text(f" Помилка: {str(e)}")

async def learn_word_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        " Вивчай нові слова або перевір свої знання!",
        reply_markup=get_learnword_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Нове слово":
        await send_random_word(update, context)
    elif text == "Назад":
        await update.message.reply_text(" Повернення в головне меню", reply_markup=get_main_keyboard())
    elif text == "Перевірити знання":
        await update.message.reply_text(" Ця функція ще в розробці.")  # За бажанням
    else:
        await update.message.reply_text(" Обери дію з меню.")

def get_handler():
    return [
        CommandHandler("learnword", learn_word_command),
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    ]