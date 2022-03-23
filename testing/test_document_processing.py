import unittest                         # библиотека для работы c юнит-тестами
from document_processing import *       # импортируем файл с методами работы с документами
from docx import Document               # библиотека для создания документов
import datetime                         # библиотека для работы со временем
from fpdf import FPDF                   # библиотека для создания PDF-файлов


# Юнит-тесты для методов скрипта работы с документами document_processing.py
class TestDocumentProcessing(unittest.TestCase):
    """
    Класс покрывает Юнит-тестами методы скрипта работы с документами document_processing.py
    """

    def setUp(self):
        """
        При определении тест-кейса TestDocumentProcessing этот метод вызывается первым

        :return: None
        """

        # сохраняем название и путь к документу и дату тестирования в атрибуты класса
        self.date = datetime.datetime.now()
        self.document_name = 'test_document_processing'
        fullname = f'{self.document_name}_{self.date}.docx'
        self.document_fullname = fullname.replace(":", "")
        self.document_path = f"D:\\Users\\Mitrol\\Desktop\\IP\\testing\\{self.document_fullname}"

        # сохраняем юрл тестовой картинки в атрибут класса
        self.vk_photo_url = 'https://sun9-59.userapi.com/impg/zYZ6g4HTf5RDvARi5QR-QJMVUVWeFTMmbbdOxg/lcOWimrVmAs.jpg?size=200x267&quality=96&sign=dfbffe0a4d0d383e89600a7a6ca7d7e8&c_uniq_tag=dHtsi6-vJ_PvxK85CDajX3Wg8PIfkILWDtmrygWmZys&type=album'

        # сохраняем юрл тестового документа в атрибут класса
        self.vk_doc_url = 'https://vk.com/doc392548774_621755651?hash=d04c11aec263d904b7&dl=GM4TENJUHA3TONA:1638369672:7a812d5f96ea8e9c3b&api=1&no_preview=1'

    def test_save_document(self):
        """
        Тестирование метода сохранения документа

        :return: Сообщение с результатом тестирования
        """

        ext = "jpg"                                                             # создаем переменную расширения файла
        file_name = self.document_name                                          # создаем переменную имени файла
        prefix = "Art"                                                          # формируем префикс файла
        right_link = rf"D:\Users\Mitrol\Desktop\IP\buffer\Art_{file_name}.jpg"  # формируем правильную ссылку на файл

        # создаем переменную с url файла
        url = self.vk_photo_url
        # созраняем файл при помощи тестируемого метода
        check_link = save_document(ext, url, file_name, prefix)

        self.assertEqual(right_link, check_link)        # сравниваем ссылки
        self.assertTrue(os.path.isfile(check_link))     # проверяем наличие файла на сервере

        if os.path.isfile(check_link):                  # если файл существует
            os.remove(check_link)                       # удаляем файл

    def test_format_bytes(self):
        """
        Тестирование метода преобразования формата бит в байты и выше

        :return: Сообщение с результатом тестирования
        """

        byte = 495648411                    # создаем условый размер файла в байтах
        set1 = format_bytes(byte)           # запускаем метод преобразования к наибольшему измерению данных
        set2 = (473, "МБ")                  # создаем кортеж правильного результата
        self.assertTupleEqual(set1, set2)   # проверяем правильность результата

    def test_process_attachment(self):
        """
        Тестирование метода обработки вложений

        :return: Сообщение с результатом тестирования
        """

        """==========Тест исхода №1=========="""
        attachment = dict()                                         # создаем словарь-описатель "приложения"
        attachment['type'] = 'txt'                                  # формируем низвестный боту типо файла
        msg = (f"Простите, с этим работать я не умею(", None)       # кортеж, который должен вернуть метод
        self.assertTupleEqual(msg, process_attachment(attachment))  # сравниваем правильный и полученный кортежи

        """==========Тест исхода №2=========="""
        url = self.vk_photo_url                                                     # устанавливаем юрл картинки для теста
        attachment = {'type': 'photo',                                        # формируем словарь-описатель "фото"
                      'photo': {'id': '457258592',
                                'sizes': [{"url": None},
                                          {"url": None},
                                          {"url": url}]}}
        link = 'D:\\Users\\Mitrol\\Desktop\\IP\\buffer\\photo_457258592.png'  # ссылка на фото, которая должна вернуться
        msg = (f'Изображение "457258592" сохранено на сервер\n'               # кортеж, который должен вернуть метод
               f'Кол-во: 1.\n'
               f'Объем: 30КБ.\n'
               f'Цена печати: 8₽.', link)

        self.assertTupleEqual(msg, process_attachment(attachment))  # сравниваем правильный и полученный кортежи

        if os.path.isfile(link):                  # если фото существует
            os.remove(link)                       # удаляем фото

        """==========Тест исхода №3=========="""
        url = self.vk_doc_url                                                       # устанавливаем юрл документа
        link = 'D:\\Users\\Mitrol\\Desktop\\IP\\buffer\\document_Метод Пиццы.pdf'   # ссылка на документ
        attachment = {'type': 'doc',                                          # формируем словарь-описатель "документа"
                      'doc': {'id': 621755651,
                              'size': 456710,
                              'url': url,
                              'ext': 'NoneName',                              # подставляем неопределенный тип данных
                              'title': 'Метод Пиццы.pdf'}}
        msg = (f'На данный момент '                                           # кортеж, который должен вернуть метод
               f'работа с таким типом данных не поддерживается(\n'     
               f'Попробуйте прикрепить файл в формате PDF или DOCX(DOC).', None)

        self.assertTupleEqual(msg, process_attachment(attachment))  # сравниваем правильный и полученный кортежи

        if os.path.isfile(link):                  # если документ существует
            os.remove(link)                       # удаляем документ

        """==========Тест исхода №4=========="""
        attachment = {'type': 'doc',                                # формируем словарь-описатель "документа"
                      'doc': {'id': 621755651,
                              'size': 456710,
                              'url': url,
                              'ext': 'pdf',
                              'title': 'Метод Пиццы.pdf'}}
        msg = (f'Документ "Метод Пиццы" сохранен на сервер!\n'  # кортеж, который должен вернуть метод
               f'Кол-во страниц в документе: 15.\n'
               f'Объем: 447КБ.\n'
               f'Цена печати: 60₽.', link)

        self.assertTupleEqual(msg, process_attachment(attachment))  # сравниваем правильный и полученный кортежи

        if os.path.isfile(link):                  # если документ существует
            os.remove(link)                       # удаляем документ

    def test_file_size(self):
        """
        Тестирование метода получения размера файла

        :return: Сообщение с результатом тестирования
        """

        size = 783                                                  # создаем константу размера нового файла
        pdf = FPDF()                                                # создаем pdf-документ
        pdf.output(self.document_fullname)                          # сохраняем pdf-документ
        self.assertEqual(file_size(self.document_path), size)       # проверяем правильность возвращаемого размера

    def test_pdf_page_count(self):
        """
        Тестирование метода получения количества страниц в PDF-документе

        :return: Сообщение с результатом тестирования
        """

        pdf = FPDF()                                                # создаем pdf-документ
        pdf.add_page()
        pdf.add_page()                                              # добавляем 3 страницы в документ
        pdf.add_page()
        pdf.output(self.document_fullname)                          # сохраняем pdf-документ
        self.assertEqual(pdf_page_count(self.document_path), 3)     # проверяем правильность подсчета страниц

        if os.path.isfile(self.document_fullname):                  # если документ ещё существует
            try:
                os.remove(self.document_fullname)                   # удаляем документ
            except:
                pass

    def test_word_page_count(self):
        """
        Тестирование метода получения количества страниц в WORD-документе

        :return: Сообщение с результатом тестирования
        """

        document = Document()                                       # создаем word-документ
        document.save(self.document_fullname)                       # сохраняем word-документ
        self.assertEqual(word_page_count(self.document_path), 1)    # проверяем правильность подсчета страниц

        if os.path.isfile(self.document_fullname):                  # если документ ещё существует
            try:
                os.remove(self.document_fullname)                   # удаляем документ
            except PermissionError:                                 # если файл используется друголй программой
                pass                                                # пока не знаю как обработать

    def test_delete_file(self):
        """
        Тестирование метода удаления файла

        :return: Сообщение с результатом тестирования
        """

        document = Document()                           # создаем word-документ
        document.save(self.document_fullname)           # сохраняем word-документ
        delete_file(self.document_fullname)             # выполняем метод удаления

        self.assertFalse(os.path.isfile(self.document_fullname))      # проверяем, удалился ли файл


# Выполнение тестов в указанных выше классах тестового случая
if __name__ == "__main__":
    unittest.main()
