# VK-Publish-Comics
Публикация комиксов на стену VK сообщества

## Как установить

Python3 должен быть установлен. Далее загрузите ряд зависимостей с помощью pip (pip3):

    pip install -r requirements.txt

Рядом с программой создайте файл `.env`. Его содержимое должно быть похожим на это:

    GROUP_ID=4567876545
    ACESS_TOKEN=1534gf5vf443345rt4cvf454ac54fdb4afe6j47g4gf7427c59deacddb

`GROUP_ID` - айди вашего сообщества. Узнать его можно [здесь](https://regvk.com/id/).

`ACESS_TOKEN` - токен вашего аккаунта. [Как его получить](https://vk.com/dev/implicit_flow_user).
Важно, чтобы у приложения были следующие права: `photos`, `groups`, `wall`, `offline` (Для этого укажите их в параметре `scope` через запятую).

## Пример успешного запуска скрипта

При успешном запуске скрипта на стене сообщества должен появиться случайный комикс.

    C:\Users\hp\VK-comics>main.py

    C:\Users\hp\VK-comics>
