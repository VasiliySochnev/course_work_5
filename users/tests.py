from django.conf import settings
from tracker.services import send_telegram_message
from django.test import TestCase
from unittest.mock import patch
import requests



class TelegramMessageTest(TestCase):
    @patch('requests.get')
    def test_send_telegram_message_success(self, mock_get):
        # Настраиваем мок-объект
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = {"ok": True}

        chat_id = "123456"
        message = "Hello, World!"

        # Вызываем функцию
        send_telegram_message(chat_id, message)

        # Проверяем, что requests.get был вызван с правильными параметрами
        mock_get.assert_called_once_with(
            f"{settings.URL_TELEGRAM}{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            params={
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "Markdown",
            }
        )

    @patch('requests.get')
    def test_send_telegram_message_failure(self, mock_get):
        # Настраиваем мок-объект для имитации ошибки
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        chat_id = "123456"
        message = "Hello, World!"

        # Вызываем функцию и ожидаем, что она не выбросит исключение
        try:
            send_telegram_message(chat_id, message)
        except Exception as e:
            self.fail(f"send_telegram_message raised Exception unexpectedly: {e}")
