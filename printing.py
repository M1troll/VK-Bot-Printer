import os                           # библиотека для работы с операционной системой (ОС)


def print_file(file):
    """
    Отправляет файл на печать

    :param file: путь к файлу на сервере
    """

    if os.path.isfile(file):                    # если файл существует
        try:
            os.startfile(file, "print")         # открываем файл в привязанной к нему программе и производим печать
        except PermissionError:                 # если файл используется друголй программой
            kill_process("WINWORD.EXE")         # принудительно закрываем word
            kill_process("Acrobat.exe")         # принудительно закрываем pdf-редактор
            os.startfile(file, "print")         # повторяем попытку
        return True                             # печать прошла успешно
    else:
        return False                            # печать не прошла


def kill_process(program_name):
    """
    Принудительно закрывает все программы с именем program_name

    :param program_name: название программы с РАЗРЕШЕНИЕМ
    """

    # принудительно завершаем процесс
    os.system(f"taskkill /f /im {program_name}")
