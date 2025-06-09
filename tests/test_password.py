import re
import pytest
import sys
import os
from unittest.mock import AsyncMock, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from handlers.password import generate_password, password_handler

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
    mock_update = MagicMock()
    mock_update.message = MagicMock()
    mock_update.message.reply_text = AsyncMock()

    # Мокаем .text.strip() корректно
    mock_text = MagicMock()
    mock_text.strip.return_value = "/password"
    mock_update.message.text = mock_text

    mock_context = MagicMock()

    await password_handler(mock_update, mock_context)

    assert mock_update.message.reply_text.call_count == 1

    args, kwargs = mock_update.message.reply_text.call_args
    assert "ваш випадковий пароль" in args[0].lower()
    assert re.search(r"`(.+)`", args[0])
