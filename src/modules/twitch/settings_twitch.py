from src.utils.logger import logger  # Импортируем кастомный логгер для записи событий
from settings.settings import get_settings_path, load_settings_by_category, TWITCH  # Импортируем функции для работы с настройками
import json  # Импортируем модуль для работы с JSON данными

def get_stream_url():
    """
    Извлекает URL-адрес Twitch трансляции из настроек TWITCH.
    """
    try:
        logger.info(f"🔄 Загрузка настроек '{TWITCH}'...")  # Логируем процесс получения настроек
        twitch_settings = load_settings_by_category(TWITCH)  # Загружаем настройки TWITCH

        # Присваиваем настройки переменным 📝
        STREAM_URL = twitch_settings.get("stream_url")  # Получаем URL Twitch трансляции

        # Проверка на наличие URL
        if not STREAM_URL:
            error_message = "Параметр 'stream_url' отсутствует в настройках TWITCH."
            logger.error(f"❌ {error_message}")  # Логируем ошибку
            raise ValueError(error_message)

        # Выводим настройки в логи 🔍
        logger.info(f"🎥 STREAM_URL: {STREAM_URL}")  # Логируем URL Twitch трансляции

        return STREAM_URL  # Возвращаем URL
    except Exception as e:  # Обработка исключений, если настройки не удалось загрузить
        logger.error(f"⚠️ Ошибка загрузки настроек '{TWITCH}': {e}", exc_info=True)  # Логируем ошибку с исключением
        raise  # Повторно генерируем исключение

def update_stream_url(new_url):
    """
    Обновляет URL-адрес Twitch трансляции в настройках TWITCH.
    """
    try:
        # Загружаем текущие настройки
        logger.info(f"🔄 Загрузка настроек '{TWITCH}'...")  # Логируем процесс получения настроек

        # Читаем текущие настройки из файла
        settings_path = get_settings_path()  # Путь к файлу настроек
        with open(settings_path, 'r') as file:
            twitch_settings = json.load(file)  # Загружаем все настройки в переменную

        # Обновляем параметр 'stream_url'
        if not new_url:
            error_message = "Новый URL не может быть пустым."
            logger.error(f"❌ {error_message}")  # Логируем ошибку
            raise ValueError(error_message)  # Генерируем исключение, если новый URL пустой

        # Обновляем URL трансляции в нужной секции
        twitch_settings["TWITCH"]["stream_url"] = new_url

        # Записываем изменения обратно в settings.json
        with open(settings_path, 'w') as file:
            json.dump(twitch_settings, file, indent=4)  # Сохраняем обновленные настройки в JSON

        logger.info(f"✅ URL обновлен: {new_url}")  # Логируем успешное обновление

    except Exception as e:
        logger.error(f"⚠️ Ошибка обновления настроек: {e}", exc_info=True)  # Логируем ошибку с исключением
        raise  # Повторно генерируем исключение