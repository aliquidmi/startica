from telegram import ReplyKeyboardMarkup, KeyboardButton

# Головне меню
def get_main_keyboard():
    keyboard = [
        [KeyboardButton("/calc"), KeyboardButton("/translate")],
        [KeyboardButton("/password"), KeyboardButton("/remind")],
        [KeyboardButton("/quote"), KeyboardButton("/advice")],
        [KeyboardButton("/learnword")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Підменю з кнопками "Ще раз" і "Назад"
def get_navigation_keyboard():
    keyboard = [
        [KeyboardButton("Назад"),
        KeyboardButton("Ще раз")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Меню для /learnword
def get_learnword_keyboard():
    keyboard = [
        [KeyboardButton("Нове слово"), KeyboardButton("Перевірити знання")],
        [KeyboardButton("Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Меню для /remind
def get_remind_keyboard():
    keyboard = [
        [KeyboardButton("Додати нагадування"), KeyboardButton("Мої нагадування")],
        [KeyboardButton("Очистити всі")],
        [KeyboardButton("Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)