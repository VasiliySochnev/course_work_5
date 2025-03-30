from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from tracker.models import Habit, Nice_Habit
from tracker.services import send_telegram_message
from users.models import User


class HabitTestCase(APITestCase):
    """Тест-кейс для тестирования CRUD-операций привычек."""

    def setUp(self):
        # Создаем пользователя который создаст привычку
        self.owner = User.objects.create(
            email="owner@mail.ru",
            password="ownerpassword",
            is_active=True,
        )
        # Создаем обычного пользователя
        self.regular_user = User.objects.create(
            email="regular@mail.ru", password="regularpassword", is_active=True
        )

        # Создаем приятную привычку, владелец будет 'owner'
        self.nice_habit = Nice_Habit.objects.create(
            owner=self.owner, action="Test nice_action", is_public=True, is_nice=True
        )

        # Создаем привычку для тестирования, владелец привычки будет 'owner'
        self.habit = Habit.objects.create(
            owner=self.owner,
            place="Test Place",
            time="00:00:00",
            action="Test Habit",
            related_habit=self.nice_habit,
            reward=None,
            execution_time="00:02:00",
            is_public=True,
        )

    # ===============================================================
    # Списки

    def test_owner_can_list_habits(self):
        """Тестирование списка привычек для владельца."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.get("/habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_can_list_nice_habits(self):
        """Тестирование списка приятных привычек для владельца."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.get("/n_habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_can_list_habits(self):
        """Тестирование списка привычек для обычного пользователя."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get("/habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_can_list_nice_habits(self):
        """Тестирование списка приятных привычек для обычного пользователя."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get("/n_habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # =====================================================================
    # Списки для владельца

    def test_owner_can_list_owner_habits(self):
        """Тестирование списка привычек созданных владельцем."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.get("/habits/own_habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_can_list_owner_nice_habits(self):
        """Тестирование списка приятных привычек созданных владельцем."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.get("/n_habits/own_n_habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ======================================================================
    # Редактирование

    def test_owner_can_edit_habit(self):
        """Тестирование редактирования привычки для владельца."""
        self.client.force_authenticate(user=self.owner)

        data = {"place": "Updated place", "action": "Updated action"}
        response = self.client.patch(f"/habits/{self.habit.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.place, "Updated place")
        self.assertEqual(self.habit.action, "Updated action")

    def test_regular_user_can_edit_habit(self):
        """Тестирование редактирования привычки для обычного пользователя."""
        self.client.force_authenticate(user=self.regular_user)
        data = {"place": "Updated place_2", "action": "Updated action_2"}
        response = self.client.patch(f"/habits/{self.habit.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_edit_nice_habit(self):
        """Тестирование редактирования приятной привычки для владельца."""
        self.client.force_authenticate(user=self.owner)
        data = {"action": "Updated action"}
        response = self.client.patch(f"/n_habits/{self.nice_habit.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.nice_habit.refresh_from_db()
        self.assertEqual(self.nice_habit.action, "Updated action")

    def test_regular_user_can_edit_nice_habit(self):
        """Тестирование редактирования приятной привычки для обычного пользователя."""
        self.client.force_authenticate(user=self.regular_user)
        data = {"action": "Updated action_2"}
        response = self.client.patch(f"/n_habits/{self.nice_habit.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_regular_user_can_update_profile(self):
        """Тестирование редактирования своего профиля."""
        self.client.force_authenticate(user=self.regular_user)
        data = {
            "email": "regular@mail.ru",
            "password": "regularpassword",
            "first_name": "Test",
        }
        response = self.client.patch(f"/users/update/{self.regular_user.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ==================================================
    # Удаление

    def test_owner_can_destroy_habit(self):
        """Тестирование удаления привычки для владельца."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(f"/habits/{self.habit.id}/")
        self.assertEqual(response.status_code, 204)

    def test_owner_can_destroy_nice_habit(self):
        """Тестирование удаления приятной привычки для владельца."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(f"/n_habits/{self.nice_habit.id}/")
        self.assertEqual(response.status_code, 204)

    def test_regular_user_can_destroy_habit(self):
        """Тестирование удаления привычки для обычного пользователя."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(f"/habits/{self.habit.id}/")
        self.assertEqual(response.status_code, 403)

    def test_regular_user_can_destroy_nice_habit(self):
        """Тестирование удаления приятной привычки для обычного пользователя."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(f"/n_habits/{self.nice_habit.id}/")
        self.assertEqual(response.status_code, 403)

    # ===============================================================
    # Создание
    def test_regular_user_can_created_habit(self):
        """Тестирование создания привычки для обычного пользователя."""
        data = {
            "place": "Test Place",
            "time": "00:00:00",
            "action": "Test Habit",
            "reward": "Test reward",
            "execution_time": "00:02:00",
            "is_public": True,
            "days_of_week": "пн",
        }
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post("/habits/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_regular_user_can_created_habit_validators(self):
        """Тестирование создания привычки для обычного пользователя c отработкой валидаторов."""
        data = {
            "place": "Test Place",
            "time": "00:00:00",
            "action": "Test Habit",
            "related_habit": 1,  # выбрана связанная привычка с вознаграждением
            "reward": "Test reward",
            "execution_time": "00:05:00",  # время больше 2 минут
            "is_public": True,
            "days_of_week": "",  # не выбранны дни недели
        }
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post("/habits/", data=data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        # Очищаем данные после теста
        self.owner.delete()
        self.regular_user.delete()
        self.habit.delete()
        self.nice_habit.delete()

    # ===============================================================
    # Отправка сообщения


class TelegramMessageTest(TestCase):
    @patch("requests.get")
    def test_send_telegram_message_success(self, mock_get):
        """Тестирование функции отправки сообщения с правильными параметрами."""
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = {"ok": True}

        chat_id = "123456"
        message = "Привет!"

        send_telegram_message(chat_id, message)

        mock_get.assert_called_once_with(
            f"{settings.URL_TELEGRAM}{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            params={
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "Markdown",
            },
        )
