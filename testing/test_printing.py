import os                   # библиотека для работы с ОС
import unittest             # библиотека для работы c юнит-тестами
from docx import Document   # библиотека для создания документов
from printing import *      # импортируем файл с методами печати
import datetime             # библиотека для работы со временем
import psutil               # библиотека для работы с системными процессами


# Юнит-тесты для методов скрипта печати printing.py
class TestPrinting(unittest.TestCase):
    """
    Класс покрывает Юнит-тестами методы скрипта печати printing.py
    """

    def setUp(self):
        """
        При определении тест-кейса TestPrinting этот метод вызывается первым

        :return: None
        """

        # сохраняем название и путь к документу и дату тестирования в атрибуты класса
        self.date = datetime.datetime.now()
        self.document_name = 'test_printing'
        fullname = f'{self.document_name}_{self.date}.docx'
        self.document_fullname = fullname.replace(":", "")
        self.document_path = f'D:/Users/Mitrol/Desktop/IP/testing/{self.document_fullname}'

    def test_print_file(self):
        """
        Тестирование метода печати файла

        :return: Сообщение с результатом тестирования
        """

        document = Document()                                # создаем word-документ
        document.save(self.document_fullname)                # сохраняем word-документ

        self.assertTrue(print_file(self.document_fullname))  # проверяем, пройдёт ли печать файла
        new_name = "Carnage = Резня.docx"                    # создаем имя несуществующего файла
        self.assertFalse(print_file(new_name))               # проверяем, пройдёт ли печать файла

        if os.path.isfile(self.document_path):               # если файл существует
            os.remove(self.document_path)                    # удаляем файл

    def test_kill_process(self):
        """
        Тестирование метода принудительного завершения процесса

        :return: Сообщение с результатом тестирования
        """

        os.open(f"{self.document_name}.docx", os.O_CREAT)     # создаем word-документ
        os.system(f'start {self.document_name}.docx')         # открываем word-документ (запускаем процесс)

        check_process = False               # флаг отсутствия процесса WORD
        kill_process("WINWORD.EXE")         # передаем WORD в метод принудительного завершения процесса

        for p in psutil.process_iter():     # пробегаемся по списку исполняемых процессов
            if "WINWORD.EXE" == p.name():   # если найден процесс программы WORD
                check_process = True        # взводим флаг о наличии такого процесса
                p.kill()                    # убиваем этот процесс

        self.assertFalse(check_process)     # проверяем флаг процесса (должен быть False)

        file = f"D:/Users/Mitrol/Desktop/IP/testing/test_printing.docx"      # путь к тестовому файлу
        if os.path.isfile(file):                                             # если файл существует
            try:
                os.remove(file)                                     # удаляем файл
            except PermissionError:                                 # если файл используется друголй программой
                pass                                                # пока не знаю как обработать


# Выполнение тестов в указанных выше классах тестового случая
if __name__ == "__main__":
    unittest.main()
