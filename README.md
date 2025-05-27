# startica

🔹 bot.py
Призначення: Головний файл запуску бота.

Що має бути:
- Імпорт Application з python-telegram-bot
- Завантаження токена з config.py
- Імпорт і реєстрація всіх обробників з handlers/
- Запуск бота через polling або webhook
- Обробка помилок

🔹 config.py
Призначення: Централізоване місце для налаштувань.

Що має бути:
- BOT_TOKEN = "..." — токен бота
- Шлях до бази даних
- API ключі, якщо потрібні (наприклад, для сторонніх сервісів)
Можливо: вибраний режим (polling/webhook)

🔹 handlers/password.py
Призначення: Команда /password — генерація випадкового безпечного пароля.

Що має бути:
- Функція password_handler(update, context)
- Локальна функція generate_password() з налаштуванням символів (великі/малі/цифри/спецсимволи)
- Відправка повідомлення з готовим паролем

🔹 handlers/quote.py
Призначення: Команди /quote і /joke — повертає випадкову цитату або жарт.

Що має бути:
- Список цитат і жартів або запит до API
- Обробник quote_or_joke_handler(update, context)
- Випадковий вибір і надсилання

🔹 handlers/learnword.py
Призначення: Команда /learnword — вивчення слів.

Що має бути:
- Словник зі словами й перекладами
- Обробник learnword_handler(update, context)
- Кнопки: повторити, зберегти слово
(Опціонально: збереження слів у базу за Telegram ID)

🔹 handlers/calc.py
Призначення: Команда /calc — обчислення математичних виразів.

Що має бути:
- Обробник calc_handler(update, context)
- Безпечний парсинг (через ast.literal_eval або вручну)
- Відправка результату або повідомлення про помилку

🔹 handlers/remind.py
Призначення: Команда /remind — збереження нагадування.


Що має бути:
- Обробник remind_handler(update, context)
- Розбір дати, часу та тексту
- Збереження нагадування в файл/базу
- Планування (через schedule або asyncio)
- Надсилання нагадування у потрібний час

🔹 handlers/advice.py
Призначення: Команда /advice — випадкова порада.

Що має бути:
- Список порад або API (наприклад, https://api.adviceslip.com/advice)
- Обробник advice_handler(update, context)
- Випадкова порада → відправка користувачу

🔹 handlers/translate.py
Призначення: Команда /translate <lang> <text> — переклад тексту на вказану мову.

Що має бути:
- Обробник translate_handler(update, context)
- Розбір параметрів (мова + текст)
- Використання googletrans (Translator().translate())
- Відправка перекладу або помилки

🔹 keyboards.py
Призначення: Кнопки меню, які зручно викликати з різних команд.

Що має бути:
- Головне меню з кнопками: Password, Quote, Learn Word, Calculator, Reminder, Advice, Translate
- Функції get_main_keyboard(), get_word_buttons() тощо
Можливо: emoji-імітація темної теми (🌙 / ☀️)