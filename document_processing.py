import requests                         # библиотека для работы с запросами и url-адресами
import PyPDF2                           # библиотека для работы с PDF-файлами
import os                               # библиотека для работы с операционной системой (ОС)
from win32com.client import Dispatch    # библиотека для работы с COM Windows и управления приложениями

from math import ceil                   # библиотека для работы с математическими операциями


def save_document(ext, url, file_name, prefix="document"):
    """
    Сохраняет документ на сервер

    :param ext: расширение файла
    :param url: url-адрес файла
    :param file_name: имя файла
    :param prefix: префикс для сохраняемого файла (по умолчанию - "document")
    :return: возвращает ссылку на сохраненный файл
    """

    r = requests.get(url)                                                      # запрашиваем документ по url-адресу
    link = rf"D:\Users\Mitrol\Desktop\IP\buffer\{prefix}_{file_name}.{ext}"    # фоормируем ссылку на документ

    with open(link, 'wb') as code:                                             # открываем документ
        code.write(r.content)                                                  # записываем результат запроса в документ

    return link                                                                # возвращаем ссылку на документ


def format_bytes(size):
    """
    Переводит байты в КБ/МБ/ГБ (до максимально возможного целочисленного)

    :param size: размер файла в байтах
    :return: множество (размер, ед. измерения)
    """

    power = 2**10                                   # 2**10 = 1024
    n = 0
    power_labels = {0: 'Б',
                    1: 'КБ',
                    2: 'МБ',
                    3: 'ГБ'}

    while size > power and n < len(power_labels):   # пока размер кратен 1024 и не превышает кол-во ед.измерения
        size /= power                               # переходим на единицу измерения выше
        n += 1

    size = ceil(size)                               # округляем результат до ближайшего целого вверх
    return size, power_labels[n]                    # возвращаем мно-во (размер, ед.измерения)


def process_attachment(attachment):
    """
    Обрабатывает вложение

    :param attachment: Словарь параметров вложения
    :return: Текст сообщения, содержащий описание документа или сведения об ошибке + ссылка на скачанный файл
    """

    # ========= Обработка документа ========== #
    if attachment['type'] == 'doc':
        doc = attachment['doc']                     # получаем параметры документа
        value, size = format_bytes(doc['size'])     # получаем размер документа и преобразуем его в больший формат
        ext = doc['ext'].lower()                    # получаем расширение документа + преобразуем его к строчному виду
        url = doc['url']                            # получаем url-адес документа
        doc_name = doc['title'].split('.')[0]       # получаем название документа
        link = save_document(ext, url, doc_name)    # сохраняем документ на сервер
        pages, cost = 0, 0                          # создаем переменные количества страниц и условной цены

        if ext in ['pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg']:       # если формат документа поддерживается
            if ext == 'pdf':                                          # если получен документ в фомате PDF
                pages = pdf_page_count(link)                          # получаем кол-во страниц в pdf-файлах
            elif ext in ['doc', 'docx']:                              # если получен документ в фомате docx, doc
                pages = word_page_count(link)                         # получаем кол-во страниц в docx(doc)-файлах

            if pages == 0:      # если кол-во страниц не изменилось, значит мы работаем с изображением
                pages = 1       # 1 изображение = 1 страница
                cost = 8        # тогда цена по умолчанию 8 рублей
            else:               # если же число страниц отлично от нуля
                cost = pages*4  # высчитываем цену: 1 страница - 4 рубля

            # возвращаем информацию о документе + ссылка на скачанный документ на сервере
            return f'Документ "{doc_name}" сохранен на сервер!\n' \
                   f"Кол-во страниц в документе: {pages}.\n" \
                   f"Объем: {value}{size}.\n" \
                   f"Цена печати: {cost}₽.", link

        else:                   # если получен другой формат
            delete_file(link)   # удаляем файл с сервера

            # возвращаем сообщение об ошибке + None (пустая ссылка)
            return f'На данный момент работа с таким типом данных не поддерживается(\n' \
                   f'Попробуйте прикрепить файл в формате PDF или DOCX(DOC).', None

    # ========== Обработка фото ========= #
    elif attachment['type'] == 'photo':
        photo = attachment['photo']                           # получаем изображение
        url = photo['sizes'][2]['url']                        # получаем url-адрес изображения [type = 'x']
        photo_id = photo['id']                                # получаем id изображения (вместо имени)
        link = save_document('png', url, photo_id, 'photo')   # сохраняем документ на сервер
        value = file_size(link)                               # получаем размер изображения
        value, size = format_bytes(value)                     # преобразуем его в больший формат

        # возвращаем информацию об изображении + ссылка на скачанное изображение на сервере
        return f'Изображение "{photo_id}" сохранено на сервер\n' \
               f"Кол-во: 1.\n" \
               f"Объем: {value}{size}.\n" \
               f"Цена печати: 8₽.", link

    # ========== Обработка других файлов ========== #
    else:
        # возвращаем сообщение об ошибке + None (пустая ссылка)
        return f"Простите, с этим работать я не умею(", None


def file_size(file):
    """
    Получает вес файла

    :param file: путь к изображению на сервере
    :return: размер файла в байтах
    """
    if os.path.isfile(file):            # если файл существует
        return os.path.getsize(file)    # получаем и возвращаем вес файла


def pdf_page_count(file):
    """
    Считает количество страниц в файле формата PDF

    :param file: путь к файлу
    :return: количество страниц в файле
    """

    with open(file, 'rb') as pdf_file:                  # открываем полученный файл
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)     # запускаем чтение pdf-файла
        pages = pdf_reader.getNumPages()                # получаем кол-во страниц в документе

    return pages                                        # возвращаем количество страниц в файле


def word_page_count(file):
    """
    Считает количество страниц в файле формата DOCX и DOC

    :param file: путь к файлу
    :return: количество страниц в файле
    """

    word = Dispatch('Word.Application')     # создаем пересенную для документа
    word.Visible = False                    # выключаем отображение ворда на экране во время запуска
    word = word.Documents.Open(file)        # открываем word

    word.Repaginate()                       # пролистываем его до конца
    pages = word.ComputeStatistics(2)       # получаем число страниц из статистики
    word.Close()                            # Закрываем ворд-документ

    return pages                            # возвращаем количество страниц в файле


def delete_file(link):
    """
    Удаляет файл с сервера

    :param link: ссылка на файл на сервере
    """

    if os.path.isfile(link):            # если файл существует
            try:
                os.remove(link)         # удаляем файл
            except PermissionError:     # если файл используется друголй программой
                pass                    # пока не знаю как обработать
