import json
from datetime import datetime, timedelta

import requests
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from config import settings


def send_telegram_message(chat_id, message):
    """Функция отправки уведомления через Телеграм-бота."""

    params = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }

    try:
        response = requests.get(
            f"{settings.URL_TELEGRAM}{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            params=params,
        )

        response.raise_for_status()

        if not response.json().get("ok"):
            print(
                f"Ошибка при отправке сообщения: {response.json().get('description')}"
            )

    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при отправке сообщения: {e}")


def set_schedule():
    """Настройки периодичности выполнения задачи."""

    # Создаем интервал для повтора
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=2,
        period=IntervalSchedule.MINUTES,
    )

    # Создаем задачу для повторения
    PeriodicTask.objects.create(
        interval=schedule,
        name="message_of_habit",
        task="tracker.tasks.message_of_habit",
        args=json.dumps(["arg1", "arg2"]),
        kwargs=json.dumps(
            {
                "be_careful": True,
            }
        ),
        expires=datetime.utcnow() + timedelta(minutes=2),
    )
