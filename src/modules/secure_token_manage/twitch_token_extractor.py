import sys  # Импортируем модуль для работы с системными путями
import os  # Импортируем модуль для работы с операционной системой
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))  # Добавляем родительский каталог в путь поиска модулей
from src.utils.logger import logger  # Импортируем логгер для записи логов

import browser_cookie3  # Импортируем библиотеку для извлечения cookies из браузеров
from settings.settings import load_settings_by_category, AUTHENTICATION_CATEGORY  # Импортируем функцию и категорию для загрузки настроек

# Инициализация переменных 🔧
USE_COOKIE_METHOD = None  # Переменная для указания метода использования cookies
BROWSER_CHOICE = None  # Переменная для выбора браузера
manual_token = None  # Переменная для хранения вручную введённого токена

# Пример использования для AUTHENTICATION 🔑
try:
    auth_settings = load_settings_by_category(AUTHENTICATION_CATEGORY)  # Загружаем настройки аутентификации
    logger.info(f"🔑 Получаем настройки 'AUTHENTICATION'...")  # Логируем процесс получения настроек

    # Присваиваем настройки переменным 📝
    USE_COOKIE_METHOD = auth_settings.get("USE_COOKIE_METHOD")  # Получаем настройку метода использования cookies
    BROWSER_CHOICE = auth_settings.get("BROWSER_CHOICE")  # Получаем выбор браузера для извлечения cookies

    # Выводим настройки в логи 🔍
    logger.info(f"🔑 USE_COOKIE_METHOD: {USE_COOKIE_METHOD}")  # Логируем метод использования cookies
    logger.info(f"🌐 BROWSER_CHOICE: {BROWSER_CHOICE}")  # Логируем выбор браузера

except Exception as e:  # Обработка исключений, если настройки не удалось загрузить
    logger.error(f"⚠️ Ошибка загрузки настроек 'AUTHENTICATION': {e}")  # Логируем ошибку загрузки настроек

# Функция для извлечения cookies из выбранного браузера 🌐
def get_browser_cookies(browser_name):  # Функция извлечения cookies по имени браузера
    """Возвращает cookies для выбранного браузера. 🍪"""
    try:
        logger.info(f"🔍 Извлекаем cookies из браузера: {browser_name}...")  # Логируем процесс извлечения cookies

        # Получаем cookies для разных браузеров 🧑‍💻
        if browser_name == "chrome":
            cookies = browser_cookie3.chrome()  # Извлекаем cookies для браузера Chrome
        elif browser_name == "chromium":
            cookies = browser_cookie3.chromium()  # Извлекаем cookies для браузера Chromium
        elif browser_name == "firefox":
            cookies = browser_cookie3.firefox()  # Извлекаем cookies для браузера Firefox
        elif browser_name == "edge":
            cookies = browser_cookie3.edge()  # Извлекаем cookies для браузера Edge
        elif browser_name == "opera":
            cookies = browser_cookie3.opera()  # Извлекаем cookies для браузера Opera
        elif browser_name == "arc":
            cookies = browser_cookie3.arc()  # Извлекаем cookies для браузера Arc
        elif browser_name == "brave":
            cookies = browser_cookie3.brave()  # Извлекаем cookies для браузера Brave
        else:
            logger.warning(f"⚠️ Поддержка для браузера {browser_name} не реализована.")  # Логируем, если браузер не поддерживается
            return None

        if cookies:  # Проверяем, были ли извлечены cookies
            logger.info(f"✅ Успешно извлечены {len(cookies)} cookies из {browser_name}.")  # Логируем успешное извлечение
            return cookies  # Возвращаем список cookies
        else:
            logger.warning(f"⚠️ Не удалось извлечь cookies из {browser_name}.")  # Логируем, если cookies не извлечены
            return None
    except Exception as e:  # Обработка ошибок при извлечении cookies
        logger.error(f"❌ Ошибка при извлечении cookies из {browser_name}: {e}", exc_info=True)  # Логируем ошибку
        return None

# Извлечение токена из cookies браузера 🔑
def get_twitch_auth_token():  # Функция для извлечения токена аутентификации Twitch
    logger.info("Получаем токен Twitch... 🔍")  # Логируем начало процесса получения токена
    """Извлекает auth-token для Twitch из cookies выбранного браузера или запрашивает вручную 📲"""
    global manual_token  # Объявляем переменную manual_token глобальной для использования в функции
    if USE_COOKIE_METHOD:  # Если выбран метод использования cookies
        try:
            logger.info(f"🔍 Ищем cookies в браузере {BROWSER_CHOICE}...")  # Логируем поиск cookies в выбранном браузере

            # Получаем cookies из выбранного браузера 🍪
            cookies = get_browser_cookies(BROWSER_CHOICE)
            if cookies:  # Если cookies были успешно извлечены
                logger.info(f"✅ Найдено {len(cookies)} cookies в {BROWSER_CHOICE}.")  # Логируем количество найденных cookies

                # Перебираем cookies и ищем нужный токен 🔑
                for cookie in cookies:
                    logger.debug(f"🔍 Проверяем cookie: {cookie.name} в домене {cookie.domain}")  # Логируем проверку каждого cookie
                    if cookie.name == "auth-token" and "twitch.tv" in cookie.domain:  # Ищем cookie с нужным именем
                        logger.info("✅ Успешно найден auth-token для Twitch.")  # Логируем, если токен найден
                        logger.info(f"🔑 Токен найден: {cookie.value[:5]}...{cookie.value[-5:]}")  # Логируем часть токена для безопасности
                        return cookie.value  # Возвращаем найденный токен

                logger.warning("⚠️ Не удалось найти auth-token среди cookies в выбранном браузере.")  # Логируем, если токен не найден
                return None
            else:
                logger.warning(f"⚠️ Не удалось извлечь cookies из {BROWSER_CHOICE}.")  # Логируем, если cookies не извлечены
                return None
        except Exception as e:  # Обработка исключений при извлечении токена
            logger.error(f"❌ Ошибка при извлечении auth-token: {e}", exc_info=True)  # Логируем ошибку
            return None
    else:  # Если используется метод ручного ввода токена
        logger.info("🔑 Используется метод ручного ввода токена. ✍️")  # Логируем, что используется метод ввода токена вручную
        if manual_token:  # Если токен уже был сохранён вручную
            logger.info("✅ Используется ранее сохранённый токен.")  # Логируем использование сохранённого токена
            logger.info(f"🔑 Введённый токен: {manual_token[:5]}...{manual_token[-5:]}")  # Логируем часть токена для безопасности
            return manual_token  # Возвращаем сохранённый токен
        else:  # Если токен не был введён
            logger.info("🔑 Пожалуйста, введите ваш auth-token вручную. ⌨️")  # Логируем запрос на ввод токена вручную
            token = input("Введите auth-token: ")  # Запрашиваем ввод токена
            if token:  # Если токен введён
                manual_token = token  # Сохраняем токен в переменной
                logger.info("✅ Токен успешно сохранён вручную. 📥")  # Логируем успешное сохранение токена
                logger.info(f"🔑 Введённый токен: {token[:5]}...{token[-5:]}")  # Логируем часть токена для безопасности
                return token  # Возвращаем введённый токен
            else:  # Если токен не был введён
                logger.warning("⚠️ Токен не был введён.")  # Логируем предупреждение, если токен не введён
                return None  # Возвращаем None, если токен не был введён