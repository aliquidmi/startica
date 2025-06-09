import pytest
import sys
import os
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from handlers import learnword

@pytest.fixture
def mock_update():
    update = MagicMock()
    update.message = MagicMock()
    update.message.reply_text = AsyncMock()
    update.effective_user.id = 123
    return update

@pytest.fixture
def mock_context():
    return MagicMock()

@pytest.mark.asyncio
async def test_show_random_word(monkeypatch, mock_update):
    monkeypatch.setattr(learnword, "load_used_words", lambda: [])
    monkeypatch.setattr(learnword, "save_used_words", lambda words: None)
    monkeypatch.setattr(learnword, "get_learnword_keyboard", lambda: None)
    monkeypatch.setattr(learnword, "DEFAULT_WORDS", [{"word": "test", "translation": "тест"}])
    monkeypatch.setattr(learnword.random, "choice", lambda lst: lst[0])

    await learnword.show_random_word(mock_update)
    mock_update.message.reply_text.assert_called_once()
    assert "test" in mock_update.message.reply_text.call_args[0][0]

@pytest.mark.asyncio
async def test_start_quiz(monkeypatch, mock_update):
    monkeypatch.setattr(learnword, "load_used_words", lambda: [{"word": "sky", "translation": "небо"}])
    monkeypatch.setattr(learnword, "get_learnword_keyboard", lambda: None)
    monkeypatch.setattr(learnword.random, "choice", lambda lst: lst[0])

    await learnword.start_quiz(mock_update)
    mock_update.message.reply_text.assert_called_once()
    assert "*sky*" in mock_update.message.reply_text.call_args[0][0]

@pytest.mark.asyncio
async def test_handle_quiz_correct_answer(monkeypatch, mock_update):
    learnword.QUIZ_STATE[123] = {"word": "sky", "translation": "небо"}
    mock_update.message.text = "небо"
    monkeypatch.setattr(learnword, "get_learnword_keyboard", lambda: None)

    await learnword.handle_quiz_answer(mock_update)
    mock_update.message.reply_text.assert_called_once()
    assert "✅ Правильно" in mock_update.message.reply_text.call_args[0][0]

@pytest.mark.asyncio
async def test_handle_quiz_wrong_answer(monkeypatch, mock_update):
    learnword.QUIZ_STATE[123] = {"word": "sky", "translation": "небо"}
    mock_update.message.text = "вода"
    monkeypatch.setattr(learnword, "get_learnword_keyboard", lambda: None)

    await learnword.handle_quiz_answer(mock_update)
    mock_update.message.reply_text.assert_called_once()
    assert "❌ Неправильно" in mock_update.message.reply_text.call_args[0][0]

@pytest.mark.asyncio
async def test_learnword_menu_handler_new_word(monkeypatch, mock_update, mock_context):
    mock_update.message.text = "Нове слово"
    monkeypatch.setattr(learnword, "show_random_word", AsyncMock())

    await learnword.learnword_menu_handler(mock_update, mock_context)
    learnword.show_random_word.assert_awaited_once()

@pytest.mark.asyncio
async def test_learnword_menu_handler_back(monkeypatch, mock_update, mock_context):
    mock_update.message.text = "Назад"
    learnword.QUIZ_STATE[123] = {"word": "abc", "translation": "xyz"}
    monkeypatch.setattr(learnword, "get_main_keyboard", lambda: None)

    await learnword.learnword_menu_handler(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once()
    assert "Головне меню" in mock_update.message.reply_text.call_args[0][0]
    assert 123 not in learnword.QUIZ_STATE
