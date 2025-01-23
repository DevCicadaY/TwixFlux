import time  # Импортируем модуль для работы с временем
import threading  # Импортируем модуль для работы с потоками
import sys  # Импортируем модуль для работы с системными функциями

# Импортируем необходимые функции и классы из модулей проекта
from src.modules.browser.browser_launcher import load_config, get_browser_options, start_browser, quit_browser, reset_global_vars  # Импорт функций для работы с браузером
from src.modules.twitch.set_auth_cookie import set_auth_cookie  # Импорт функции для установки cookies
from src.modules.twitch.open_stream import open_stream  # Импорт функции для открытия стрима
from src.modules.twitch.bonus_clicker import get_bonus  # Импорт функции для получения бонусов
from src.modules.browser.close_browser_after_timeout import close_browser  # Импорт функции для закрытия браузера по таймеру
from src.utils.clean_pycache import remove_pycache_in_project  # Импорт функции для очистки кэша Python
from src.utils.logger import logger  # Импортируем логгер для записи сообщений
from src.modules.secure_token_manage.token_storage_manager import AUTH_TOKEN  # Импортируем токен авторизации
from src.modules.twitch.settings_twitch import get_stream_url  # Импорт функции для получения URL стрима
from src.modules.twitch.auto_shutdown_timer import auto_shutdown_browser

# Главная функция для запуска процесса работы с Twitch
def twitch_main():
    try:
        logger.info("🚀 Запуск Twitch Main Process...")  # Логируем начало процесса

        # Загрузка конфигурации
        logger.info("📄 Загружаем конфигурацию...")  # Логируем загрузку конфигурации
        config = load_config()  # Загружаем конфигурацию из файла
        logger.info("✅ Конфигурация успешно загружена!")  # Логируем успешную загрузку конфигурации

        # Получаем настройки из конфигурации
        browser_mode = config["browser_mode"]  # Режим браузера из конфигурации
        chrome_driver_path = config["chrome_driver_path"]  # Путь к драйверу Chrome из конфигурации
        auth_token = AUTH_TOKEN  # Получаем токен авторизации
        stream_url = get_stream_url()  # Получаем URL стрима

        # Получаем настройки для браузера
        logger.info("🛠️ Настраиваем параметры браузера...")  # Логируем настройку параметров браузера
        options = get_browser_options(browser_mode)  # Получаем параметры для браузера в зависимости от режима
        logger.info(f"✅ Параметры настроены: режим = {browser_mode}")  # Логируем успешную настройку параметров

        # Запускаем браузер
        logger.info("🌐 Запускаем браузер...")  # Логируем запуск браузера
        driver = start_browser(chrome_driver_path, options)  # Запускаем браузер с заданными параметрами
        logger.info("✅ Браузер успешно запущен!")  # Логируем успешный запуск браузера

        # Устанавливаем cookies для авторизации
        logger.info("🍪 Устанавливаем cookies для авторизации...")  # Логируем установку cookies
        set_auth_cookie(driver, auth_token)  # Устанавливаем cookies для авторизации в браузере
        logger.info("✅ Cookies успешно установлены!")  # Логируем успешную установку cookies

        # Открываем стрим
        logger.info("📺 Открываем стрим...")  # Логируем начало открытия стрима
        open_stream(driver, stream_url)  # Открываем стрим по заданному URL
        logger.info("✅ Стрим успешно открыт!")  # Логируем успешное открытие стрима

        # Получаем значение таймера выключения браузера
        timeout_seconds = auto_shutdown_browser()

        # Преобразуем значение в минуты
        timeout_minutes = timeout_seconds # Конвертируем секунды в минуты

        sleep_time = timeout_seconds  # Для примера, оставим значение в секундах

        # Преобразуем таймер в минуты, если нужно
        minutes = timeout_seconds  # Используем полученные минуты

        # Логируем
        logger.info(f"Значение таймера выключения браузера: {timeout_seconds} секунд, {timeout_minutes} минут(ы).")

        # Логируем
        logger.info(f"Таймер в секундах: {timeout_minutes} секунд, Таймер в минутах: {minutes} минут(ы), Время сна в секундах: {sleep_time} секунд")

        # Получаем бонусы
        logger.info("🎁 Начинаем получать бонусы...")  # Логируем начало получения бонусов
        get_bonus(driver, timeout_minutes, sleep_time)  # Начинаем процесс получения бонусов
        logger.info("✅ Бонусы успешно получены!")  # Логируем успешное получение бонусов

        # Закрываем браузер через минуту
        logger.info("⏳ Запускаем таймер для закрытия браузера...")  # Логируем начало отсчета времени для закрытия
        close_browser(driver, minutes)  # Запускаем таймер на закрытие браузера через 1 минуту
        logger.info("✅ Браузер будет закрыт через 1 минуту.")  # Логируем, что браузер будет закрыт через минуту

        logger.info("🎉 Завершение работы Twitch Main Process!")  # Логируем завершение работы основного процесса

        reset_global_vars()  # Сбрасываем глобальные переменные для чистоты состояния
    except Exception as e:  # Обрабатываем возможные ошибки
        logger.error(f"❌ Ошибка: {e}")  # Логируем ошибку, если она произошла