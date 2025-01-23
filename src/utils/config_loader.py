import json  # Импортируем модуль для работы с JSON
import os  # Импортируем модуль для работы с операционной системой
from src.utils.logger import logger  # Импортируем объект логгера для записи логов

def load_config():
    """
    Загружает конфигурационный файл в формате JSON.

    :return: Данные из конфигурационного файла в виде словаря.
    :raises FileNotFoundError: Если файл не найден.
    :raises json.JSONDecodeError: Если файл содержит некорректный JSON.
    """
    # Получаем путь к корню проекта
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))  # Определяем абсолютный путь к корню проекта
    
    # Формируем путь к файлу конфигурации в папке 'config'
    config_path = os.path.join(project_root, 'config', 'browser_launcher.json')  # Путь к конфигурационному файлу в папке 'config'
    
    if not os.path.exists(config_path):  # Проверка существования файла
        logger.error(f"❌ Файл конфигурации не найден: {config_path}")  # Логируем ошибку, если файл не существует
        raise FileNotFoundError(f"❌ Файл конфигурации не найден: {config_path}")  # Выбрасываем исключение, если файл не найден
    
    try:
        # Открываем файл и загружаем JSON-данные
        with open(config_path, 'r', encoding='utf-8') as config_file:  # Открываем файл для чтения с указанием кодировки UTF-8
            configuration = json.load(config_file)  # Загружаем содержимое файла как JSON
            logger.info(f"✅ Конфигурация успешно загружена из {config_path}.")  # Логируем успешную загрузку конфигурации
            return configuration  # Возвращаем загруженные данные как словарь
    except json.JSONDecodeError as decode_error:  # Обрабатываем ошибку декодирования JSON
        logger.error(f"❌ Ошибка декодирования JSON в файле {config_path}: {decode_error}")  # Логируем ошибку при декодировании
        raise  # Пробрасываем исключение, чтобы его обработал вызывающий код