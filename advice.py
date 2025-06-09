import random, logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from keyboards import get_main_keyboard

logger = logging.getLogger(__name__)

REPEAT_ADVICE_TEXT = "Ще порада"

ADVICES = [
    "Не чекай ідеального моменту — він може ніколи не настати. Починай з того, що маєш, і вдосконалюйся в процесі.",
    "Роби перерви кожні 25-30 хвилин — мозок працює ефективніше, коли має змогу відпочити. Спробуй техніку Помодоро.",
    "Складай список справ на день — це допоможе уникнути прокрастинації та тримати фокус на важливому.",
    "Не намагайся вивчити все за один вечір — розподіляй навчання рівномірно, і знання закріпляться краще.",
    "Спочатку виконуй найскладніші завдання — ранкова концентрація допомагає впоратись із важким набагато швидше.",
    "Не перевантажуй себе — ефективніше робити 2-3 важливі справи на день, ніж намагатися встигнути все й нічого не завершити.",
    "Вчися розуміти, а не зубрити — знання, які ти осмислив, залишаться з тобою надовго.",
    "Повторюй матеріал через 1-2 дні після вивчення — так утворюються довготривалі спогади.",
    "Очищуй робоче місце перед початком — порядок навколо допомагає зосередитись і впорядковує думки.",
    "Не забувай про здоровий сон — навіть найкраще вивчене вночі забувається, якщо організм виснажений.",
    "Пиши конспекти своїми словами — так ти краще зрозумієш тему й зможеш швидко повторити основне.",
    "Використовуй кольорові виділення чи стікери — це допомагає структурувати інформацію та краще запам'ятати.",
    "Навчися казати 'ні' зайвим справам — твій час обмежений, тож витрачай його на важливе.",
    "Спілкуйся з однодумцями — навчання в команді іноді ефективніше, ніж на самоті.",
    "Не бійся помилок — вони частина навчання. Аналізуй їх і вчися на них.",
    "Рухайся під час перерв — прогулянка або легка зарядка освіжить думки та підвищить продуктивність.",
    "Пиши собі мотиваційні нотатки — короткі фрази, що нагадують, чому ти це робиш.",
    "Харчуйся регулярно та збалансовано — мозку потрібна енергія для обробки інформації.",
    "Не зосереджуйся лише на оцінках — важливіше те, що ти справді зрозумів і запам’ятав.",
    "Пам’ятай, ти вже на правильному шляху — кожне зусилля наближає тебе до цілі, навіть якщо результат не одразу помітний."
]

def get_advice_keyboard():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("Назад"), KeyboardButton(REPEAT_ADVICE_TEXT)]],
        resize_keyboard=True
    )

async def advice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        text = update.message.text.strip()
        logger.info(f"Отримано повідомлення: '{text}'")

        if text in ["/advice", "💡 Порада", REPEAT_ADVICE_TEXT]:
            if not ADVICES:
                await update.message.reply_text("⚠️ Список порад порожній.")
                logger.warning("Запит /advice, але список порад порожній.")
                return

            advice = random.choice(ADVICES)
            await update.message.reply_text(f'✨ {advice}', reply_markup=get_advice_keyboard())
            logger.info("Надіслано випадкову пораду користувачу.")

        elif text == "Назад":
            await update.message.reply_text("Головне меню:", reply_markup=get_main_keyboard())
            logger.info("Користувач повернувся у головне меню.")

        else:
            logger.debug(f"Непідтримуваний ввід у advice_handler: '{text}' — ігнорується.")

    except Exception as e:
        logger.exception(f"❌ Помилка в advice_handler: {e}")
        await update.message.reply_text("❌ Сталася помилка при обробці поради.")

def get_handler():
    return [
        CommandHandler("advice", advice_handler),
        MessageHandler(
            filters.TEXT & filters.Regex(rf"^(💡 Порада|{REPEAT_ADVICE_TEXT}|Назад|/advice)$"),
            advice_handler
        )
    ]
