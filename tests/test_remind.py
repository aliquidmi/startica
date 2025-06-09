import pytest
import sys
import os
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from handlers import remind

@pytest.fixture
def mock_update():
    update = MagicMock()
    update.message = MagicMock()
    update.message.from_user.id = 123
    update.message.reply_text = AsyncMock()
    return update

@pytest.fixture
def mock_context():
    ctx = MagicMock()
    ctx.args = []
    ctx.application = MagicMock()
    return ctx

@pytest.mark.asyncio
async def test_remind_command_invalid_format(mock_update, mock_context):
    mock_context.args = ["2024-01-01"]
    await remind.remind_command(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once()
    assert "неправильний формат" in mock_update.message.reply_text.call_args[0][0]

@pytest.mark.asyncio
async def test_remind_command_past_date(mock_update, mock_context):
    mock_context.args = ["2000-01-01", "00:00", "тест"]
    await remind.remind_command(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once()
    assert "у майбутньому" in mock_update.message.reply_text.call_args[0][0]

@pytest.mark.asyncio
async def test_remind_command_success(monkeypatch, mock_update, mock_context):
    now = datetime.now() + timedelta(minutes=1)
    mock_context.args = [now.strftime("%Y-%m-%d"), now.strftime("%H:%M"), "перевірка"]
    
    monkeypatch.setattr(remind, "save_reminder", lambda *a, **kw: 1)
    monkeypatch.setattr(remind, "schedule_reminder", lambda *a, **kw: None)

    await remind.remind_command(mock_update, mock_context)
    mock_update.message.reply_text.assert_called()
    assert "Нагадування встановлено" in mock_update.message.reply_text.call_args[0][0]

@pytest.mark.asyncio
async def test_show_reminders_empty(monkeypatch, mock_update, mock_context):
    monkeypatch.setattr(remind, "get_user_reminders", lambda uid: [])
    await remind.show_reminders(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once()
    assert "немає активних нагадувань" in mock_update.message.reply_text.call_args[0][0].lower()

@pytest.mark.asyncio
async def test_clear_reminders(monkeypatch, mock_update, mock_context):
    monkeypatch.setattr(remind, "clear_user_reminders", lambda uid: 2)
    monkeypatch.setattr(remind.scheduler, "get_jobs", lambda: [])
    await remind.clear_reminders(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once()
    assert "видалено 2" in mock_update.message.reply_text.call_args[0][0].lower()
