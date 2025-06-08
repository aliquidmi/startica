import logging, sqlite3
from datetime import datetime
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from keyboards import get_main_keyboard, get_remind_keyboard

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_FILE = 'reminders.db'
scheduler = AsyncIOScheduler()

def start_scheduler():
    if not scheduler.running:
        scheduler.start()

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            remind_time TEXT NOT NULL,
            text TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def save_reminder(user_id: int, remind_time: str, text: str):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO reminders (user_id, remind_time, text) VALUES (?, ?, ?)', (user_id, remind_time, text))
        conn.commit()
        reminder_id = cursor.lastrowid
        conn.close()
        logger.info(f"Нагадування збережено: user_id={user_id}, time={remind_time}, text={text}")
        return reminder_id
    except Exception as e:
        logger.error(f"Помилка збереження нагадування: {e}")
        return None

def get_user_reminders(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, remind_time, text FROM reminders WHERE user_id=? ORDER BY remind_time', (user_id,))
    reminders = cursor.fetchall()
    conn.close()
    return reminders

def clear_user_reminders(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM reminders WHERE user_id=?', (user_id,))
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    logger.info(f"Видалено {deleted} нагадувань користувача {user_id}")
    return deleted

async def send_reminder(context: ContextTypes.DEFAULT_TYPE, job_data):
    user_id = job_data['user_id']
    text = job_data['text']
    reminder_id = job_data['reminder_id']

    try:
        await context.bot.send_message(chat_id=user_id, text=f"⏰ Нагадування:\n{text}")
        logger.info(f"Надіслано нагадування користувачу {user_id}: {text}")
    except Exception as e:
        logger.error(f"Помилка надсилання нагадування користувачу {user_id}: {e}")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM reminders WHERE id=?', (reminder_id,))
    conn.commit()
    conn.close()

    job = context.job
    if job:
        job.remove()

def schedule_reminder(reminder_id: int, user_id: int, remind_time: datetime, text: str, application):
    run_date = remind_time
    scheduler.add_job(
        send_reminder,
        'date',
        run_date=run_date,
        args=[application],
        id=str(reminder_id),
        replace_existing=True,
        misfire_grace_time=60,
        kwargs={'job_data': {'user_id': user_id, 'text': text, 'reminder_id': reminder_id}}
    )
    logger.info(f"Заплановано нагадування id={reminder_id} на {run_date}")

async def remind_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.message.from_user.id
        args = context.args

        if len(args) < 3:
            await update.message.reply_text("❗ Помилка: неправильний формат.\n\nВикористання:\n/remind <YYYY-MM-DD> <HH:MM> <текст нагадування>")
            return

        date_str = args[0]
        time_str = args[1]
        text = ' '.join(args[2:])

        try:
            remind_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            await update.message.reply_text("❗ Помилка: дата або час мають бути у форматі YYYY-MM-DD HH:MM")
            return

        if remind_datetime <= datetime.now():
            await update.message.reply_text("❗ Помилка: дата та час мають бути у майбутньому.")
            return

        reminder_id = save_reminder(user_id, remind_datetime.isoformat(), text)
        if reminder_id is None:
            await update.message.reply_text("❗ Сталася помилка при збереженні нагадування.")
            return

        schedule_reminder(reminder_id, user_id, remind_datetime, text, context.application)

        await update.message.reply_text(f"✅ Нагадування встановлено на {remind_datetime.strftime('%Y-%m-%d %H:%M')}:\n{text}")

    except Exception as e:
        logger.error(f"Помилка у remind_command: {e}")
        await update.message.reply_text("❗ Сталася невідома помилка. Спробуйте пізніше.")

async def show_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.message.from_user.id
        reminders = get_user_reminders(user_id)
        if not reminders:
            await update.message.reply_text("У вас немає активних нагадувань.")
            return

        msg_lines = ["📝 Ваші нагадування:"]
        for rid, dt_str, text in reminders:
            dt = datetime.fromisoformat(dt_str)
            msg_lines.append(f"- ID {rid}: {dt.strftime('%Y-%m-%d %H:%M')} — {text}")

        await update.message.reply_text('\n'.join(msg_lines))

    except Exception as e:
        logger.error(f"Помилка у show_reminders: {e}")
        await update.message.reply_text("❗ Сталася помилка при отриманні нагадувань.")

async def clear_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.message.from_user.id
        deleted = clear_user_reminders(user_id)
        if deleted == 0:
            await update.message.reply_text("У вас немає нагадувань для видалення.")
        else:
            for job in scheduler.get_jobs():
                if str(user_id) in job.id:
                    job.remove()
            await update.message.reply_text(f"✅ Видалено {deleted} нагадувань.")
    except Exception as e:
        logger.error(f"Помилка у clear_reminders: {e}")
        await update.message.reply_text("❗ Сталася помилка при видаленні нагадувань.")

async def remind_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Додати нагадування":
        await update.message.reply_text(
            "Введіть команду у форматі:\n/remind <YYYY-MM-DD> <HH:MM> <текст нагадування>",
            reply_markup=get_remind_keyboard()
        )
    elif text == "Мої нагадування":
        await show_reminders(update, context)
    elif text == "Очистити всі":
        await clear_reminders(update, context)
    elif text == "Назад":
        await update.message.reply_text("Повернення в головне меню", reply_markup=get_main_keyboard())
    else:
        await update.message.reply_text("Невідома команда, оберіть зі списку.", reply_markup=get_remind_keyboard())

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📆 Нагадування":
        await update.message.reply_text(
            "Оберіть дію:",
            reply_markup=get_remind_keyboard()
        )

def get_handler():
    return [
        CommandHandler("remind", remind_command),
        MessageHandler(filters.TEXT & filters.Regex(r"^(Додати нагадування|Мої нагадування|Очистити всі|Назад)$"), remind_menu_handler),
        MessageHandler(filters.TEXT & filters.Regex(r"^📆 Нагадування$"), main_menu_handler),
    ]