# VK-Bot-Printer
Bot for VKontakte social network that allows you to print documents and photos sent to him.

## Функционал

The bot accepts messages in the VKontakte group. 
If the message is one of the commands ("распечатай", "распечатать", "принт", "печать", "print")
and contains an attached file of supported formats (.doc, .docx, .pdf, .png, .JPEG, .JPG), then the Bot will start its work.

After sending the message, the bot will download the image or document. Initializes the file data and sends the user a response containing information about the file and the cost of printing. The user will also see two buttons: "Печать" and "Отмена".

| Photo | Document |
|:---------:|:---------:|
|![Alt-текст](https://sun9-85.userapi.com/impf/YkrnnXcPF7jCDAQgoc0TLYPlpPI2Iyj4eBBBuQ/qh4cJsfcfj4.jpg?size=720x1600&quality=96&sign=854fda3036382dc21eae54d2cd669dec&type=album)|![Alt-текст](https://sun9-80.userapi.com/impf/4KjvHfQ1xKMsu_wJHaEBrO9UThR93CxHlI1Qyw/N1hgZFwB4J8.jpg?size=720x1600&quality=96&sign=9e5ad19d8113c76f7eece5ad176bb566&type=album)|

When you click on the "Отмена" button, the bot will cancel the printing operation, delete the file from server and the buttons from the dialog, and then notify the user about the cancellation of the operation.

| Photo | Document |
|:---------:|:---------:|
|![Alt-текст](https://sun9-77.userapi.com/impf/tXhFy47ZaVxSP90h6JrdLqSTDxb9t56CJLATyw/PKpSl5hTw44.jpg?size=720x1600&quality=96&sign=39b5e27dd67af1936a1db22150ce61c4&type=album)|![Alt-текст](https://sun9-56.userapi.com/impf/aanntEKwvZ_55MlSAhAu3tVfwHDB9UaDMtAXug/5hLvJyq8oL8.jpg?size=720x1600&quality=96&sign=5cba6c53c9a529c5021a1ebbeea3a76d&type=album)|

When you click on the "Печать" button, the bot will display a stub message "Let's imagine that you paid :point_right::point_left:" (in the future, instead of a stub, it is planned to connect the vk_pay service provided by the Vkontakte api, which will allow the user to pay for printing using any electronic wallet or card) and the printing process will begin.

| Photo | Document |
|:---------:|:---------:|
|![Alt-текст](https://sun9-87.userapi.com/impf/ATuZtUwki-DP3d5GnDOtQqsK6KYPw7lLo0RXdw/Y4ybxKs4uUU.jpg?size=720x1600&quality=96&sign=fcefd2ca51b486c3b137fdc45729b70e&type=album)|![Alt-текст](https://sun9-20.userapi.com/impf/ASL0Fh849IEkuxdYTc_5WzBFX-2RR0v12NjXAg/GdYCAO06Vv8.jpg?size=720x1600&quality=96&sign=83a35c1ef814e2e0021065e058ddf64f&type=album)|

Before printing, the action buttons will also be removed from the dialog, and upon completion of the process, the user will receive an alert.
| Photo | Document |
|:---------:|:---------:|
|![Alt-текст](https://sun9-51.userapi.com/impf/doitF71Mww8Anb7UVpPkyd2Ph401Up_aNqV-Dg/0K81nFFzM4I.jpg?size=720x1600&quality=96&sign=cc726581a8b5bb99a026bfcbe2d4aaf6&type=album)|![Alt-текст](https://sun9-85.userapi.com/impf/TDg_RPh47QypYjDvZANcr_jlQwexLhk1A1qO8g/4BO6WmdaP5s.jpg?size=720x1600&quality=96&sign=000bb5ea10326bdf8d7b157f711f2c7d&type=album)|

## Unit tests - Юнит тесты
The bot has partial unit test coverage.
