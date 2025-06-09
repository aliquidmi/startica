import logging, re, math
from telegram.ext import CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from keyboards import get_main_keyboard

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("calc")

WAITING_FORMULA = 1

def get_calc_keyboard():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("Ще раз"), KeyboardButton("Назад")]],
        resize_keyboard=True
    )

def safe_eval(expression):
    logger.info(f"Оцінка виразу: {expression}")
    expr = expression.replace(' ', '').replace(',', '.')
    functions = {
        'sqrt': 'math.sqrt', 'sin': 'math.sin', 'cos': 'math.cos', 'tan': 'math.tan',
        'log': 'math.log', 'ln': 'math.log', 'log10': 'math.log10', 'exp': 'math.exp',
        'pow': 'pow', 'abs': 'abs', 'pi': 'math.pi', 'e': 'math.e'
    }
    for k, v in functions.items():
        expr = expr.replace(k, v)
    if not re.fullmatch(r'[0-9+\-*/()._a-zA-Z]+', expr):
        raise ValueError("Недозволені символи у виразі")
    try:
        return eval(expr, {"__builtins__": {}, "math": math, "pow": pow, "abs": abs, "round": round})
    except Exception as e:
        raise ValueError(f"Помилка обчислення: {e}")

def format_result(result):
    if isinstance(result, float):
        return (f"{int(result):,}" if result.is_integer()
                else f"{result:.10f}".rstrip('0').rstrip('.').replace('.', ','))
    return f"{result:,}".replace(',', ' ')

async def calc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"/calc від {update.effective_user.id}, args={context.args}")
    try:
        if context.args:
            return await process_calculation(update, context, ' '.join(context.args))
        await update.message.reply_text(
            "<b>\U0001F9EE Калькулятор</b>\n\n"
            "Введіть математичний вираз для обчислення.\n\n"
            "<b>Підтримувані операції:</b>\n"
            "• Основні: +, -, *, /, ( )\n"
            "• Функції: sqrt, sin, cos, tan, log, ln, exp, pow, abs\n"
            "• Константи: pi, e\n\n"
            "<b>Приклади:</b>\n"
            "• <code>2 + 2 * 3</code>\n"
            "• <code>sqrt(16) + pow(2, 3)</code>\n"
            "• <code>sin(pi/2) * cos(0)</code>",
            parse_mode='HTML', reply_markup=get_calc_keyboard()
        )
        return WAITING_FORMULA
    except Exception as e:
        logger.error(f"Помилка в calc_command: {e}")
        await update.message.reply_text("❌ Сталася помилка при запуску калькулятора.")
        return ConversationHandler.END

async def process_calculation(update: Update, context: ContextTypes.DEFAULT_TYPE, formula: str):
    if not formula.strip():
        await update.message.reply_text("❌ Порожній вираз! Введіть щось.", reply_markup=get_calc_keyboard())
        return WAITING_FORMULA
    try:
        result = safe_eval(formula)
        formatted = format_result(result)
        await update.message.reply_text(
            f"✅ <b>Результат:</b>\n\n"
            f"<b>Формула:</b> <code>{formula}</code>\n"
            f"<b>Відповідь:</b> <code>{formatted}</code>",
            parse_mode='HTML', reply_markup=get_calc_keyboard()
        )
        logger.info(f"✅ {formula} = {formatted}")
    except ValueError as e:
        logger.warning(f"⚠️ Невірний ввід: {formula} -> {e}")
        await update.message.reply_text(
            f"❌ <b>Помилка:</b> {e}", parse_mode='HTML', reply_markup=get_calc_keyboard()
        )
    except Exception as e:
        logger.error(f"❌ Помилка '{formula}': {e}")
        await update.message.reply_text(
            "❌ <b>Синтаксична помилка!</b> Перевірте вираз.",
            parse_mode='HTML', reply_markup=get_calc_keyboard()
        )
    return WAITING_FORMULA

async def handle_formula_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    logger.info(f"Ввід користувача: {text}")
    if text == "Назад":
        return await go_back(update, context)
    elif text == "Ще раз":
        return await try_again(update, context)
    return await process_calculation(update, context, text)

async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Назад від {update.effective_user.id}")
    await update.message.reply_text("Головне меню:", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def try_again(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Повторний запуск калькулятора від {update.effective_user.id}")
    return await calc_command(update, context)

async def cancel_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Скасування калькулятора {update.effective_user.id}")
    await update.message.reply_text("Калькулятор закрито.", reply_markup=get_main_keyboard())
    return ConversationHandler.END

def get_handler():
    return ConversationHandler(
        entry_points=[MessageHandler(filters.Regex(r"^\U0001F9EE Калькулятор$"), calc_command)],
        states={
            WAITING_FORMULA: [
                MessageHandler(filters.Regex(r"^Назад$"), go_back),
                MessageHandler(filters.Regex(r"^Ще раз$"), try_again),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_formula_input)
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel_calc)],
        name="calc_conversation",
        persistent=False
    )
