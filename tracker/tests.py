from rest_framework.test import APITestCase
from datetime import time
from tracker.models import Habit, Nice_Habit
from users.models import User
from rest_framework import status

class HabitTestCase(APITestCase):
    """Тест-кейс для тестирования CRUD-операций привычек."""

    def setUp(self):
        # Создаем пользователя который создаст привычку
        self.owner = User.objects.create(
            email="owner@mail.ru", password="ownerpassword", tg_chat_id=633017007, is_active=True
        )
        # Создаем обычного пользователя
        self.regular_user = User.objects.create(
            email="regular@mail.ru", password="regularpassword", is_active=True
        )

        def default_time_0():
            return time(0, 0)

        def default_time_2():
            return time(0, 2)

        # Создаем приятную привычку, владелец будет 'owner'
        self.nice_habit = Nice_Habit.objects.create(
            owner=self.owner,
            action="Test nice_action",
            is_public=True,
            is_nice=True
        )

        # Создаем привычку для тестирования, владелец привычки будет 'owner'
        self.habit = Habit.objects.create(
            owner=self.owner,
            place="Test Place",
            time=default_time_0(),
            action="Test Habit",
            related_habit=self.nice_habit,
            reward=None,
            execution_time=default_time_2(),
            is_public=True,
            days_of_week={'пн, вт, ср'}
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
        response = self.client.get("/n_habit/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_can_list_habits(self):
        """Тестирование списка привычек для обычного пользователя."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get("/habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_can_list_nice_habits(self):
        """Тестирование списка приятных привычек для обычного пользователя."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get("/n_habit/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# =====================================================================
# Списки для владельца

    def test_owner_can_list_owner_habits(self):
        """Тестирование списка привычек созданных владельцем."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.get("/own_habit/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_owner_can_list_owner_nice_habits(self):
        """Тестирование списка приятных привычек созданных владельцем."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.get("/own_n_habit/")
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
        self.assertEqual(self.habit.action, "Updated action")  # Проверяем обновление

    # def test_regular_user_can_edit_habit(self):
    #     """Тестирование редактирования привычки для обычного пользователя."""
    #     self.client.force_authenticate(user=self.regular_user)
    #     data = {"place": "Updated place_2", "action": "Updated action_2"}
    #     response = self.client.patch(f"/habits/{self.habit.id}/", data)
    #     print(response.json())
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_owner_can_edit_nice_habit(self):
        """Тестирование редактирования приятной привычки для владельца."""
        self.client.force_authenticate(user=self.owner)
        data = {"action": "Updated action"}
        response = self.client.patch(f"/n_habit/update/{self.nice_habit.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.nice_habit.refresh_from_db()
        self.assertEqual(self.nice_habit.action, "Updated action")  # Проверяем обновление


    def test_regular_user_can_edit_nice_habit(self):
        """Тестирование редактирования приятной привычки для обычного пользователя."""
        self.client.force_authenticate(user=self.regular_user)
        data = {"action": "Updated action_2"}
        response = self.client.patch(f"/n_habit/update/{self.nice_habit.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


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
        response = self.client.delete(f"/n_habit/delete/{self.nice_habit.id}/")
        self.assertEqual(response.status_code, 204)


    def test_regular_user_can_destroy_habit(self):
        """Тестирование удаления привычки для обычного пользователя."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(f"/habits/{self.habit.id}/")
        self.assertEqual(response.status_code, 403)


    def test_regular_user_can_destroy_nice_habit(self):
        """Тестирование удаления приятной привычки для обычного пользователя."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(f"/n_habit/delete/{self.nice_habit.id}/")
        self.assertEqual(response.status_code, 403)


    def tearDown(self):
        # Очищаем данные после теста
        self.owner.delete()
        self.regular_user.delete()
        self.habit.delete()
        self.nice_habit.delete()