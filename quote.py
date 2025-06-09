import random, logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters
from keyboards import get_main_keyboard

logger = logging.getLogger(__name__)

REPEAT_QUOTE_TEXT = "Ще цитата"

QUOTES = [
    '"Успіх — це не кінець, поразка — не фатальна: важлива лише мужність продовжувати." — Вінстон Черчилль',
    '"Працюй мовчки. Нехай успіх говорить за тебе." — Франк Оушен',
    '"Не чекай ідеального моменту — створи його сам." — Джордж Бернард Шоу (приблизна інтерпретація)',
    '"Великі мрії роблять великі досягнення." — Норман Вінсент Піл',
    '"Хто хоче — шукає можливості, хто не хоче — шукає причини." — невідомий автор',
    '"Тільки той, хто йде, здолає дорогу." — народна мудрість',
    '"Щоб дійти до мети, потрібно насамперед іти." — Оноре де Бальзак',
    '"Зміни починаються з тебе." — Майкл Джексон (відомо з пісні «Man in the Mirror»)',
    '"Не бійся помилок — бійся бездіяльності." — Джон Вуден',
    '"Кожен день — новий шанс змінити життя." — невідомий автор',
    '"Ти сильніший, ніж думаєш." — Крістофер Робін (з творів А. А. Мілна)',
    '"Падав — вставай. Впав знову — вставай швидше." — Вин Дизель (відоме з інтерв`ю)',
    '"Щастя — це шлях, а не пункт призначення." — Рой М. Гудман',
    '"Людина стає тим, у що вона вірить." — Махатма Ганді',
    '"Немає нічого неможливого для того, хто прагне." — Александр Македонський',
    '"Дій, навіть якщо боїшся." — Шеріл Сендберг',
    '"Ніколи не пізно почати з початку." — Джоел Остін',
    '"Успіх приходить до тих, хто діє." — Наполеон Гілл',
    '"Мрій масштабно, дій впевнено." — Тоні Роббінс',
    '"Кожна спроба — це крок до мети." — Томас Едісон'
]

def get_quote_keyboard():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("Назад"), KeyboardButton(REPEAT_QUOTE_TEXT)]],
        resize_keyboard=True
    )

async def quote_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        text = update.message.text
        logger.info(f"Отримано повідомлення: '{text}'")

        if text in ["/quote", "😄 Цитата", REPEAT_QUOTE_TEXT]:
            if not QUOTES:
                await update.message.reply_text("⚠️ Список цитат порожній.")
                logger.warning("Запит /quote, але список цитат порожній.")
                return

            quote = random.choice(QUOTES)
            await update.message.reply_text(f'💡 {quote}', reply_markup=get_quote_keyboard())
            logger.info("Надіслано випадкову цитату користувачу.")

        elif text == "Назад":
            await update.message.reply_text("Головне меню:", reply_markup=get_main_keyboard())
            logger.info("Користувач повернувся у головне меню.")

        else:
            logger.debug(f"Непідтримуваний ввід у quote_handler: '{text}' — ігнорується.")

    except Exception as e:
        logger.error(f"❌ Помилка в quote_handler: {e}")
        await update.message.reply_text("❌ Сталася помилка при обробці цитати.")

def get_handler():
    return [
        CommandHandler("quote", quote_handler),
        MessageHandler(
            filters.TEXT & filters.Regex(rf"^(😄 Цитата|{REPEAT_QUOTE_TEXT}|Назад|/quote)$"),
            quote_handler
        )
    ]
