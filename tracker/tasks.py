from datetime import datetime

from celery import shared_task
from django.utils import timezone

from .models import Habit
from .services import send_telegram_message


@shared_task
def message_of_habit():
    # Получаем текущий день недели в формате 'пн', 'вт', 'ср' и т.д.
    today = datetime.now().strftime("%a").lower()  # Пример: 'mon', 'tue', 'wed'
    current_time = timezone.now().time()

    # Словарь для перевода английских сокращений на русский
    days_translation = {
        "mon": "пн",
        "tue": "вт",
        "wed": "ср",
        "thu": "чт",
        "fri": "пт",
        "sat": "сб",
        "sun": "вс",
    }

    # Переводим сегодняшний день на русский
    today_russian = days_translation[today]

    # Получаем привычки, которые соответствуют сегодняшнему дню
    habits = Habit.objects.filter(days_of_week__icontains=today_russian)

    for habit in habits:
        if habit.owner.tg_chat_id:
            chat_id = habit.owner.tg_chat_id

            # Проверяем, если текущее время больше или равно времени привычки
            if current_time >= habit.time:
                if habit.reward != None:
                    message = f"Напоминание: пора {habit.action}, за это можешь {habit.reward}"
                    send_telegram_message(chat_id, message)
                else:
                    message = f"Напоминание: пора {habit.action}, за это можешь {habit.related_habit}"
                    send_telegram_message(chat_id, message)
