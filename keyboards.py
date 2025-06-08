from telegram import ReplyKeyboardMarkup, KeyboardButton

# Головне меню
def get_main_keyboard():
    keyboard = [
        [KeyboardButton("🧮 Калькулятор"), KeyboardButton("🌍 Перекладач")],
        [KeyboardButton("🔐 Генератор паролів"), KeyboardButton("📆 Нагадування")],
        [KeyboardButton("😄 Цитата"), KeyboardButton("💡 Порада")],
        [KeyboardButton("📚 Вивчення слів")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# "Ще раз" / "Назад" (скопійюте для свого коду)
def get_navigation_keyboard():
    keyboard = [
        [KeyboardButton("Назад"),
        KeyboardButton("Ще раз")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# /learnword
def get_learnword_keyboard():
    keyboard = [
        [KeyboardButton("Нове слово"), KeyboardButton("Перевірити знання")],
        [KeyboardButton("Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# /remind
def get_remind_keyboard():
    keyboard = [
        [KeyboardButton("Додати нагадування"), KeyboardButton("Мої нагадування")],
        [KeyboardButton("Очистити всі")],
        [KeyboardButton("Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
