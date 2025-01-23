import logging  # Импортируем стандартный модуль для логирования в Python
import json  # Импортируем модуль для работы с JSON данными
from src.utils.logger import logger  # Импортируем кастомный логгер для записи событий, определенный в src/utils/logger.py
from settings.settings import get_settings_path, load_settings_by_category, BROWSER_SETTINGS  # Импортируем функции и константы из настроек

# Функция для загрузки настроек браузера
def load_browser_settings():
    """
    Загружает настройки из категории 'BROWSER_SETTINGS'.

    Описание:
        Эта функция читает настройки браузера из указанной категории настроек 
        и возвращает их в виде словаря.

    Возвращает:
        dict: Настройки браузера, если загрузка выполнена успешно.
        None: Если произошла ошибка при чтении настроек.
    """
    try:
        logger.info("🔧 Начинаем загрузку настроек 'BROWSER_SETTINGS'...")
        browser_settings = load_settings_by_category(BROWSER_SETTINGS)  # Чтение настроек
        logger.info(f"✅ Настройки успешно загружены: {browser_settings}")
        return browser_settings
    except Exception as e:
        # Логируем ошибку, если загрузить настройки не удалось
        logger.error(f"❌ Ошибка при загрузке настроек 'BROWSER_SETTINGS': {e}")
        return None

# Функция для получения значения AUTO_SHUTDOWN_TIMER
def auto_shutdown_browser():
    """
    Получает значение параметра 'AUTO_SHUTDOWN_TIMER' из настроек.

    Описание:
        Эта функция отвечает за поиск и получение значения параметра 
        'AUTO_SHUTDOWN_TIMER' из категории настроек браузера.
        Если настройка отсутствует или не загружена, выводит соответствующее предупреждение.

    Действия:
        1. Загружает настройки с помощью `load_browser_settings`.
        2. Проверяет наличие параметра 'AUTO_SHUTDOWN_TIMER'.
        3. Логирует значение параметра или предупреждение об ошибке.

    Возвращает:
        None
    """
    try:
        # Загружаем настройки браузера
        browser_settings = load_browser_settings()
        if browser_settings is None:
            logger.warning("⚠️ Настройки 'BROWSER_SETTINGS' не были загружены. Значение 'AUTO_SHUTDOWN_TIMER' недоступно.")
            return

        # Проверяем наличие параметра AUTO_SHUTDOWN_TIMER
        auto_shutdown_timer = browser_settings.get("AUTO_SHUTDOWN_TIMER")
        if auto_shutdown_timer is None:
            logger.warning("⚠️ Параметр 'AUTO_SHUTDOWN_TIMER' отсутствует в настройках.")
            return

        # Логируем успешное получение значения
        logger.info(f"⏱️ Значение 'AUTO_SHUTDOWN_TIMER' успешно получено: {auto_shutdown_timer} секунд.")
        return auto_shutdown_timer  # Возвращаем значение таймера
    except Exception as e:
        # Логируем ошибку при обработке параметра
        logger.error(f"❌ Произошла ошибка при получении значения 'AUTO_SHUTDOWN_TIMER': {e}")

def update_auto_shutdown_timer(time):
    """
    Обновляет параметр 'auto_shutdown_timer' в настройках 'BROWSER_SETTINGS'.
    """
    try:
        # Загружаем текущие настройки
        logger.info(f"🔄 Загрузка настроек '{BROWSER_SETTINGS}'...")  # Логируем процесс получения настроек

        # Читаем текущие настройки из файла
        settings_path = get_settings_path()  # Путь к файлу настроек
        with open(settings_path, 'r') as file:
            settings = json.load(file)  # Загружаем все настройки в переменную

        # Проверяем, что 'BROWSER_SETTINGS' существует в настройках
        if "BROWSER_SETTINGS" not in settings:
            error_message = "'BROWSER_SETTINGS' не найдены в настройках."
            logger.error(f"❌ {error_message}")
            raise ValueError(error_message)

        # Обновляем параметр 'auto_shutdown_timer' в секции 'BROWSER_SETTINGS'
        settings["BROWSER_SETTINGS"]["AUTO_SHUTDOWN_TIMER"] = time

        # Записываем изменения обратно в settings.json
        with open(settings_path, 'w') as file:
            json.dump(settings, file, indent=4)  # Сохраняем обновленные настройки в JSON

        logger.info(f"✅ Параметр 'auto_shutdown_timer' обновлен: {time} секунд.")  # Логируем успешное обновление

    except Exception as e:
        logger.error(f"⚠️ Ошибка обновления настроек: {e}", exc_info=True)
        raise
