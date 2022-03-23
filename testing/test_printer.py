import unittest                                         # библиотека для работы c юнит-тестами
from printer import *                                   # импортируем файл с главными методами Бота


# Юнит-тесты для методов главного скрипта printer.py
class TestPrinter(unittest.TestCase):
    """
    Класс покрывает Юнит-тестами методы главного скрипта printer.py
    """

    def setUp(self):
        """
        При определении тест-кейса TestPrinter этот метод вызывается первым

        :return: None
        """

        # инициализируем атрибуты класса для группы
        self.vk_session = vk_api.VkApi(token=GROUP_TOKEN, api_version=API_VERSION)  # инициируем сессию ВКонтакте
        self.vk = self.vk_session.get_api()                                         # получаем API

        # инициализируем атрибуты класса для личных сообщений
        self.ls_session = vk_api.VkApi(token=MY_TOKEN, api_version=API_VERSION)
        self.ls_vk = self.ls_session.get_api()

    def test_send_message(self):
        """
        Тестирование метода отправки сообщений

        :return: Сообщение с результатом тестирования
        """

        # проверяем на исключения метод отправки сообщений
        self.assertRaises(BaseException, send_message(MY_ID, message="Приём! Проверка! Меня слышно?"))
        # получаем текст последнего пришедшего сообщения
        message = self.vk.messages.getHistory(count=1,
                                              user_id=MY_ID,
                                              peer_id=MY_ID)['items'][0]['text']
        self.assertEqual("Приём! Проверка! Меня слышно?", message)          # проверяем, верно ли дошло сообщение
        self.delete_message(group=True)                                     # удаляем отправленное выше сообщения

    def test_initialization(self):
        """
        Тестирование метода инициализации бота

        :return: Сообщение с результатом тестирования
        """

        # отправляем тестовое сообщение № 1
        message = "Абра-К@daBRa25846"
        self.ls_vk.messages.send(peer_id=-GROUP_ID,
                                 random_id=get_random_id(),
                                 message=message)
        self.delete_message(ls=True)                                        # удаляем тестовое сообщение №1
        self.assertEqual("Я не знаю такой команды 😢", initialization())    # проверяем правильность ответа бота
        self.delete_message(group=True)                                     # удаляем ответ бота

        # отправляем тестовое сообщение № 2
        message = "Распечатай"
        self.ls_vk.messages.send(peer_id=-GROUP_ID,
                                 random_id=get_random_id(),
                                 message=message)
        self.delete_message(ls=True)                                        # удаляем тестовое сообщение №2
        self.assertEqual("Вы не прикрепили документ(", initialization())    # проверяем правильность ответа бота
        self.delete_message(group=True)                                     # удаляем ответ бота

        # отправляем тестовое сообщение № 3
        message = "()"
        self.ls_vk.messages.send(peer_id=-GROUP_ID,
                                 random_id=get_random_id(),
                                 message=message)
        self.delete_message(ls=True)                                        # удаляем тестовое сообщение №3
        self.assertEqual("👉🏻👈🏻", initialization())                           # проверяем правильность ответа бота
        self.delete_message(group=True)                                     # удаляем ответ бота

    def delete_message(self, ls=False, group=False):
        """
        Удаялет последнее отправленное сообщение
        :param ls: Если True, то удаляется последнее личное сообщение
        :param group: Если True, то удаляется последнее сообщение сообщества
        :return: None
        """

        if group:
            # получаем идентификатор последнего отправленного сообщения сообщества
            message_id = self.vk.messages.getHistory(count=1,
                                                     user_id=MY_ID,
                                                     peer_id=MY_ID)['items'][0]['id']
            # удаляем сообщение
            self.vk.messages.delete(message_ids=message_id,
                                    delete_for_all=1,
                                    peer_id=MY_ID)
        if ls:
            # получаем идентификатор последнего отправленного сообщения пользователя
            message_id = self.ls_vk.messages.getHistory(count=1,
                                                        user_id=-GROUP_ID,
                                                        peer_id=-GROUP_ID)['items'][0]['id']
            # удаляем сообщение
            self.ls_vk.messages.delete(message_ids=message_id,
                                       delete_for_all=1,
                                       peer_id=-GROUP_ID)


# Выполнение тестов в указанных выше классах тестового случая
if __name__ == "__main__":
    unittest.main()
