MY_TOKEN = 'Your VK profile token - токен от Вашего профиля ВКонтакте'  # https://vkhost.github.io
GROUP_TOKEN = "Your VK group token - токен от Вашей группы ВКонтакте"   # https://vkhost.github.io
API_VERSION = "5.131"

GROUP_ID = 0    # ID your VK group - ID Вашей группы ВКонтакте            https://regvk.com/id/
MY_ID = 0       # ID your VK profile - ID Вашего профиля ВКонтакте        https://regvk.com/id/

USER_AGENT = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                            'AppleWebKit/537.11 (KHTML, like Gecko) '
                            'Chrome/23.0.1271.64 Safari/537.11',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
              'Accept-Encoding': 'none',
              'Accept-Language': 'en-US,en;q=0.8',
              'Connection': 'keep-alive'}

# определяем список команд
COMMANDS = ["распечатай", "распечатать", "принт", "печать", "print"]

# коллекции тематических стикеров
STICKERS = {
    'ору': [8637, 12119, 56772],
    'че': [56779, 3170, 14755, 13897, 63431],
    'обида': [73, 8804, 53368, 54158, 108],
    'крутой': [63427, 62938, 63428, 60780, 61166, 60265, 52312, 61, 21789, 3154],
    'подумай': [21789]
}

# виды callback-кнопок
CALLBACK_TYPES = ('show_snackbar', 'open_link', 'open_app')
