import re
import pytest
from handlers.password import generate_password, password_handler
from unittest.mock import AsyncMock, MagicMock

# ---------- TEST 1: generate_password ----------

def test_generate_password_length():
    password = generate_password()
    assert 8 <= len(password) <= 16

def test_generate_password_characters():
    password = generate_password()
    assert any(c.isdigit() for c in password)
    assert any(c.isalpha() for c in password)
    assert any(not c.isalnum() for c in password)  # спецсимволы

# ---------- TEST 2: password_handler ----------

@pytest.mark.asyncio
async def test_password_handler_response():
    # Создаём mock update.message.reply_text
    mock_update = MagicMock()
    mock_update.message.reply_text = AsyncMock()

    mock_context = MagicMock()

    await password_handler(mock_update, mock_context)

    # Проверяем, что reply_text был вызван
    assert mock_update.message.reply_text.call_count == 1

    # Проверяем, что ответ содержит пароль в `` (markdown)
    args, kwargs = mock_update.message.reply_text.call_args
    assert "ваш випадковий пароль" in args[0].lower()
    assert re.search(r"`(.+)`", args[0])  # пароль в `` Markdown
