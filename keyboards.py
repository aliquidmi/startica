from telegram import ReplyKeyboardMarkup, KeyboardButton

# 🔹 Головне меню
def get_main_keyboard():
    keyboard = [
        [KeyboardButton("/calc")],
        [KeyboardButton("/learnword")],
        [KeyboardButton("/help")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# 🔹 Меню для /learnword
def get_learnword_keyboard():
    keyboard = [
        [KeyboardButton("Нове слово"),
         KeyboardButton("Перевірити знання")],
        [KeyboardButton("Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# 🔹 Інше підменю (можна розширити, для цього потрібно скопіювати функцію і змінити назву функції та кнопок)
def get_example_submenu():
    keyboard = [
        [KeyboardButton("Опція 1"),
         KeyboardButton("Опція 2")],
        [KeyboardButton("Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
