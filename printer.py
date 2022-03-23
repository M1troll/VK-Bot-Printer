from config import *                    # импортируем файл с настройками для бота
from document_processing import *       # импортируем файл с методами обработки документов
from printing import *                  # импортируем файл с методами печати документов
import os                               # библиотека для работы с ОСс методами удаления файлов
import shutil                           # библиотека с методами удаления файлов
import json                             # библиотека для работы с json
from time import sleep                  # библиотека для врмененной имитации ассинхронного программирования

# ===== Импортируем API с его методами ===== #
import vk_api
# from vk_api.longpoll import VkLongPoll, VkEventType                  # для работыв личных сообщениях
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType          # для работы с сообществами
from vk_api.utils import get_random_id                                 # метод для получения случайного id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor                # классы для работы с callback-кнопками

# ===== Авторизаця в боте ===== #
vk_session = vk_api.VkApi(token=GROUP_TOKEN, api_version=API_VERSION)  # инициируем сессию ВКонтакте
vk = vk_session.get_api()                                              # получаем API
longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)                # список всех событий


def send_message(user_id, message="Такова жизнь",
                 attachment=None, keyboard=None):
    """
    Отправляет сообщение пользователю

    :param user_id: id пользователя, которому нужно отправить сообщение
    :param message: текст сообщения
    :param attachment: вложения (по умолчанию - None)
    :param keyboard: прикрепленные к сообщению кнопки (по умолчанию - None)
    """

    vk.messages.send(user_id=user_id,
                     random_id=get_random_id(),
                     message=message,
                     attachment=attachment,
                     keyboard=keyboard)


def initialization():
    """
    Главный метод: слушает и реагирует на события

    :return: Ответное сообщение
    """

    for event in longpoll.listen():                    # слушаем события
        if event.type == VkBotEventType.MESSAGE_NEW:   # если это новое сообщение
            msg = event.obj.message['text'].lower()    # получаем текст сообщения
            user_id = event.obj.message['from_id']     # получаем id отправителя

            # парсим 1й прикреплённый документ
            attachments = event.obj.message['attachments']

            if msg in COMMANDS:     # если сообщение является командой
                if attachments:     # если есть прикрепленный файл

                    attachment = attachments[0]                         # получаем информацию о 1ом вложении сообщения
                    answer, file = process_attachment(attachment)       # получаем сведения о файлк и путь к нему
                    keyboard = None                                     # создаем переменную для будущеё клавиатуры

                    if file is not None:                               # если файл был успешно скачан
                        settings = dict(one_time=False, inline=True)    # настройки для клавиатуры
                        keyboard = VkKeyboard(**settings)              # создаем клавиатуру для кнопок

                        # добавляем кнопку "Печать"
                        keyboard.add_callback_button(label='Печать',
                                                     color=VkKeyboardColor.POSITIVE,
                                                     payload={"type": "show_snackbar",
                                                              "text": "Давайте представим, что вы оплатили 👉🏻👈🏻",
                                                              "file": file})
                        # добавляем отступ после кнопки
                        keyboard.add_line()
                        # добавляем кнопку "Отмена"
                        keyboard.add_callback_button(label='Отмена',
                                                     color=VkKeyboardColor.NEGATIVE,
                                                     payload={"type": "cancel",
                                                              "file": file})
                        # получаем сформированную клавиатуру
                        keyboard = keyboard.get_keyboard()

                    # отправляем сообщение об успешной печати или ошибке
                    send_message(user_id, answer, attachment, keyboard)
                    return answer                                           # возвращаем текст ответного сообщения
                else:                                                       # если нет прикрепленного файла
                    send_message(user_id, "Вы не прикрепили документ(")     # сообщаем об ошибке
                    return "Вы не прикрепили документ("                     # возвращаем текст ответного сообщения
            elif msg == "()":
                send_message(user_id, "👉🏻👈🏻")   # Пасхалка
                return "👉🏻👈🏻"                   # возвращаем текст ответного сообщения
            else:
                send_message(user_id, "Я не знаю такой команды 😢")     # обработка неизвестных команд
                return "Я не знаю такой команды 😢"                     # возвращаем текст ответного сообщения

        # обрабатываем клики по callback кнопкам
        elif event.type == VkBotEventType.MESSAGE_EVENT:

            button_type = event.object.payload.get('type')              # определяем тип нажатой кнопки
            event_id = event.object.event_id                            # определяем id события
            user_id = event.object.user_id                              # определяем id пользователя, нажавшего кнопку
            peer_id = event.object.peer_id                              # определяем id диалога
            file = event.object.payload.get('file')                     # получаем путь к файлу на сервере
            conversation_msg_id = event.obj.conversation_message_id     # определяем id изменяемого сообщения

            # получаем содержимое сообщения по conversation_message_id и peer_id
            message = vk_session.method("messages.getByConversationMessageId",
                                        {"peer_id": peer_id, "conversation_message_ids": [conversation_msg_id, ]})
            # определяем текст сообщения
            text = message['items'][0]['text']

            # если это одно из 3х встроенных действий:
            if button_type in CALLBACK_TYPES:
                payload = event.object.payload  # получаем содержание payload
                payload.pop('file', 666)        # удаляем лишний элемент из payload
                # выполняем действия, заложенные в payload
                vk.messages.sendMessageEventAnswer(
                        event_id=event_id,
                        user_id=user_id,
                        peer_id=peer_id,
                        event_data=json.dumps(payload))
                print_file(file)                                            # отправляем файл на печать
                sleep(5)                                                    # ожидаем завершения печати
                send_message(user_id, "Процедура печати была завершена")    # отправляем сообщение о завершении печати
            # если это "кастомная" кнопка
            elif button_type == 'cancel':
                send_message(user_id, "Процедура печати была отменена")     # отправляем сообщение об отмене печати

            # редактируем сообщение - удаляем кнопки
            vk.messages.edit(
                    peer_id=peer_id,
                    message=f'{text}\n\n[Действия больше недоступны]',
                    conversation_message_id=conversation_msg_id,
                    keyboard=None)
            delete_file(file)   # удаляем файл с сервера
            clear_buffer()          # чистим буфер сервера


def clear_buffer():
    """
    Чистит буфер сервера

    :return: None
    """

    # сохраняем путь к папке буфера обмена
    folder = "buffer"
    # перебираем содержимое папки
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                # удаляем файлы
                os.unlink(file_path)
        except Exception as e:
            # в случае ошибки - выводим её в терминал
            print(e)


if __name__ == '__main__':  # точка входа
    while True:
        initialization()        # инициализируем проверку списка событий
