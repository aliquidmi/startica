import pytest
import sys
import os
from unittest.mock import AsyncMock, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from handlers.advice import advice_handler, REPEAT_ADVICE_TEXT

@pytest.fixture
def mock_update():
    update = MagicMock()
    update.message = MagicMock()
    update.message.reply_text = AsyncMock()
    return update

@pytest.fixture
def mock_context():
    return MagicMock()

@pytest.mark.asyncio
async def test_send_random_advice(monkeypatch, mock_update, mock_context):
    mock_update.message.text = "/advice"

    test_advice = "Це тестова порада"
    monkeypatch.setattr("handlers.advice.ADVICES", [test_advice])
    monkeypatch.setattr("handlers.advice.random.choice", lambda x: test_advice)

    await advice_handler(mock_update, mock_context)

    mock_update.message.reply_text.assert_called_once()
    args, _ = mock_update.message.reply_text.call_args
    assert test_advice in args[0]

@pytest.mark.asyncio
async def test_back_button(mock_update, mock_context):
    mock_update.message.text = "Назад"

    await advice_handler(mock_update, mock_context)

    mock_update.message.reply_text.assert_called_once()
    args, _ = mock_update.message.reply_text.call_args
    assert "Головне меню" in args[0]

@pytest.mark.asyncio
async def test_unknown_text_ignored(mock_update, mock_context):
    mock_update.message.text = "незрозуміло"

    await advice_handler(mock_update, mock_context)

    mock_update.message.reply_text.assert_not_called()

@pytest.mark.asyncio
async def test_empty_advices(monkeypatch, mock_update, mock_context):
    mock_update.message.text = "/advice"
    monkeypatch.setattr("handlers.advice.ADVICES", [])

    await advice_handler(mock_update, mock_context)

    mock_update.message.reply_text.assert_called_once()
    args, _ = mock_update.message.reply_text.call_args
    assert "порад порожній" in args[0].lower()
