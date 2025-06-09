import pytest
import sys
import os
from unittest.mock import AsyncMock, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from handlers import translate as t

@pytest.fixture
def mock_update():
    update = MagicMock()
    update.message = MagicMock()
    update.message.text = "en Привіт"
    update.message.reply_text = AsyncMock()
    return update

@pytest.fixture
def mock_context():
    ctx = MagicMock()
    ctx.args = []
    return ctx

class MockTranslator:
    def __init__(self, **kwargs):
        pass
    def translate(self, text):
        return "Hello"

@pytest.mark.asyncio
async def test_translate_command_success(monkeypatch, mock_update, mock_context):
    mock_context.args = ["en", "Привіт"]
    monkeypatch.setattr(t, "GoogleTranslator", MockTranslator)

    await t.translate_command(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once()
    assert "Переклад" in mock_update.message.reply_text.call_args[0][0]

@pytest.mark.asyncio
async def test_translate_command_invalid_args(mock_update, mock_context):
    mock_context.args = ["en"]
    await t.translate_command(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once()
    assert "формат" in mock_update.message.reply_text.call_args[0][0].lower()

@pytest.mark.asyncio
async def test_text_message_handler_success(monkeypatch, mock_update, mock_context):
    monkeypatch.setattr(t, "GoogleTranslator", MockTranslator)
    mock_update.message.text = "en Привіт"

    await t.text_message_handler(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once()
    assert "Переклад" in mock_update.message.reply_text.call_args[0][0]

@pytest.mark.asyncio
async def test_text_message_handler_unknown_lang(mock_update, mock_context):
    mock_update.message.text = "xx Привіт"
    await t.text_message_handler(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once()
    assert "невідома мова" in mock_update.message.reply_text.call_args[0][0].lower()

@pytest.mark.asyncio
async def test_text_message_handler_empty_text(mock_update, mock_context):
    mock_update.message.text = "en"  # только 1 слово

    await t.text_message_handler(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once()
    assert "недостатньо інформації" in mock_update.message.reply_text.call_args[0][0].lower()


@pytest.mark.asyncio
async def test_translate_button_handler(mock_update, mock_context):
    await t.translate_button_handler(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once()
    assert "Підтримувані мови" in mock_update.message.reply_text.call_args[0][0]
