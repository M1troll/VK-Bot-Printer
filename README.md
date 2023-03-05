### Languages: [RU](https://github.com/M1troll/VK-Bot-Printer/blob/main/README.md)| [EN](https://github.com/M1troll/VK-Bot-Printer/blob/main/README_EN.md)

# VK-Bot-Printer
Бот для социальной сети ВКонтакте, позволяющий распечатывать присланные ему документы и фотографии.

## Функционал

Бот принимает сообщения в группе ВКонтакте. 
Если сообщение является одной из команд ("распечатай", "распечатать", "принт", "печать", "print") 
и содержит вложенный файл поддерживаемых форматов (.doc, .docx, .pdf, .png, .JPEG, .JPG), то Бот начнет свою работу.

После отправки сообщения Бот скачает изображение или документ. Проалализирует данные файла и отправит пользователю ответ, содержащий информацию о файле и стоимости печати. Также пользователю выведутся две кнопки: "Печать" и "Отмена".

| Photo | Document |
|:---------:|:---------:|
|![Alt-текст](https://sun9-85.userapi.com/impf/YkrnnXcPF7jCDAQgoc0TLYPlpPI2Iyj4eBBBuQ/qh4cJsfcfj4.jpg?size=720x1600&quality=96&sign=854fda3036382dc21eae54d2cd669dec&type=album)|![Alt-текст](https://sun9-80.userapi.com/impf/4KjvHfQ1xKMsu_wJHaEBrO9UThR93CxHlI1Qyw/N1hgZFwB4J8.jpg?size=720x1600&quality=96&sign=9e5ad19d8113c76f7eece5ad176bb566&type=album)|

При нажатии на кнопку "Отмена" бот отменит операцию печати, удалит файл с "сервера" и кнопки из диалога, после чего оповестит пользователя об отмене операции.

| Photo | Document |
|:---------:|:---------:|
|![Alt-текст](https://sun9-77.userapi.com/impf/tXhFy47ZaVxSP90h6JrdLqSTDxb9t56CJLATyw/PKpSl5hTw44.jpg?size=720x1600&quality=96&sign=39b5e27dd67af1936a1db22150ce61c4&type=album)|![Alt-текст](https://sun9-56.userapi.com/impf/aanntEKwvZ_55MlSAhAu3tVfwHDB9UaDMtAXug/5hLvJyq8oL8.jpg?size=720x1600&quality=96&sign=5cba6c53c9a529c5021a1ebbeea3a76d&type=album)|

При нажатии же на кнопку "Печать" Бот выведет сообщение-заглушку "Давайте представим, что вы оплатили :point_right::point_left:" (в будущем, вместо заглушки планируется подключение сервиса vk_pay, предоставляемого api Вконтакте, что позволит пользователю оплачивать печать с помошью любого электронного кошелька или карты) и начнется процесс печати.

| Photo | Document |
|:---------:|:---------:|
|![Alt-текст](https://sun9-87.userapi.com/impf/ATuZtUwki-DP3d5GnDOtQqsK6KYPw7lLo0RXdw/Y4ybxKs4uUU.jpg?size=720x1600&quality=96&sign=fcefd2ca51b486c3b137fdc45729b70e&type=album)|![Alt-текст](https://sun9-20.userapi.com/impf/ASL0Fh849IEkuxdYTc_5WzBFX-2RR0v12NjXAg/GdYCAO06Vv8.jpg?size=720x1600&quality=96&sign=83a35c1ef814e2e0021065e058ddf64f&type=album)|

Перед печатью из диалога также удалятся кнопки действий, а по завершению процесса пользователь получит оповещение.
| Photo | Document |
|:---------:|:---------:|
|![Alt-текст](https://sun9-51.userapi.com/impf/doitF71Mww8Anb7UVpPkyd2Ph401Up_aNqV-Dg/0K81nFFzM4I.jpg?size=720x1600&quality=96&sign=cc726581a8b5bb99a026bfcbe2d4aaf6&type=album)|![Alt-текст](https://sun9-85.userapi.com/impf/TDg_RPh47QypYjDvZANcr_jlQwexLhk1A1qO8g/4BO6WmdaP5s.jpg?size=720x1600&quality=96&sign=000bb5ea10326bdf8d7b157f711f2c7d&type=album)|

## Unit tests - Юнит тесты
Бот имеет частичное покрытие юнит тестами.
