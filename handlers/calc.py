from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import re

# Дозволені символи: цифри, + - * / ( ) і пробіли
ALLOWED_EXPR_PATTERN = r'^[\d\s+\-*/().]+$'

def is_valid_expression(expr: str) -> bool:
    return re.match(ALLOWED_EXPR_PATTERN, expr) is not None

def safe_eval(expr: str) -> float:
    return eval(expr, {"__builtins__": None}, {})

async def calc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    expr = ' '.join(context.args)

    if not expr:
        await update.message.reply_text(
            "Введи вираз після /calc. Наприклад: `/calc 2 + 3 * (4 - 1)`",
            parse_mode='Markdown'
        )
        return

    if not is_valid_expression(expr):
        await update.message.reply_text("Вираз містить недопустимі символи. Дозволено: цифри, + - * / ( )")
        return

    try:
        result = safe_eval(expr)
        await update.message.reply_text(f"Результат: {result}")
    except SyntaxError:
        await update.message.reply_text("Синтаксична помилка у виразі.")
    except Exception as e:
        await update.message.reply_text(f"Помилка при обчисленні: {str(e)}")

def get_handler():
    return CommandHandler("calc", calc_command)
