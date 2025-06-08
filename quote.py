from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
import random
import logging
from keyboards import get_navigation_keyboard, get_main_keyboard

# Ініціалізуємо лог
logger = logging.getLogger(name)

# Локальний список цитат
QUOTES = [
    "Успіх — це не кінець, поразка — не фатальна: важлива лише мужність продовжувати. — Вінстон Черчилль",
    "Працюй мовчки. Нехай успіх говорить за тебе. — Франк Оушен",
    "Не чекай ідеального моменту — створи його сам. — Джордж Бернард Шоу (приблизна інтерпретація)",
    "Великі мрії роблять великі досягнення. — Норман Вінсент Піл",
    "Хто хоче — шукає можливості, хто не хоче — шукає причини. — невідомий автор",
    "Тільки той, хто йде, здолає дорогу. — народна мудрість",
    "Щоб дійти до мети, потрібно насамперед іти. — Оноре де Бальзак",
    "Зміни починаються з тебе. — Майкл Джексон (відомо з пісні «Man in the Mirror»)",
    "Не бійся помилок — бійся бездіяльності. — Джон Вуден",
    "Кожен день — новий шанс змінити життя. — невідомий автор",
    "Ти сильніший, ніж думаєш. — Крістофер Робін (з творів А. А. Мілна)",
    "Падав — вставай. Впав знову — вставай швидше. — Вин Дизель (відоме з інтерв'ю)",
    "Щастя — це шлях, а не пункт призначення. — Рой М. Гудман",
    "Людина стає тим, у що вона вірить. — Махатма Ганді",
    "Немає нічого неможливого для того, хто прагне. — Александр Македонський",
    "Дій, навіть якщо боїшся. — Шеріл Сендберг",
    "Ніколи не пізно почати з початку. — Джоел Остін",
    "Успіх приходить до тих, хто діє. — Наполеон Гілл",
    "Мрій масштабно, дій впевнено. — Тоні Роббінс",
    "Кожна спроба — це крок до мети. — Томас Едісон",
    "Роби те, що любиш — і ти ніколи не працюватимеш. — Конфуцій"
]


# Обробник /quote
async def quote_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        text = update.message.text

        if text == "/quote" or text == "Ще раз":
            if not QUOTES:
                await update.message.reply_text("⚠️ Список цитат порожній.")
                logger.warning("Запит /quote, але список цитат порожній.")
                return

            quote = random.choice(QUOTES)
            keyboard = get_navigation_keyboard()
            await update.message.reply_text(f'💡 "{quote}"', reply_markup=keyboard)
            logger.info("Надіслано випадкову цитату користувачу.")

        elif text == "Назад":
            keyboard = get_main_keyboard()
            await update.message.reply_text("Повернулись у головне меню.", reply_markup=keyboard)
            logger.info(f"Користувач повернувся у головне меню.")

        else:
            await update.message.reply_text(
                "Введи /quote або натисни кнопку.",
                reply_markup=get_navigation_keyboard()
            )
            logger.warning(f"Користувач надіслав невідому команду: {text}")

    except Exception as e:
        logger.error(f"Помилка в quote_handler: {e}")
        await update.message.reply_text("⚠️ Виникла помилка при отриманні цитати.")