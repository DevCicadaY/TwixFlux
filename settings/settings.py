import sys  # Модуль для работы с системными параметрами
import os  # Модуль для работы с операционной системой (пути, файлы и т.д.)
import shutil  # Модуль для копирования и удаления файлов
import json  # Модуль для работы с JSON данными
from src.utils.logger import logger  # Импорт логгера для записи сообщений
from pathlib import Path  # Модуль для работы с путями и директориями

# Переменные для категорий конфигурации
AUTHENTICATION_CATEGORY = "AUTHENTICATION"  # Категория для аутентификации
ENCRYPTION_CATEGORY = "encryption"  # Категория для шифрования
TWITCH = "TWITCH"  # Категория для Twitch
BROWSER_SETTINGS = "BROWSER_SETTINGS"  # Категория для настроек браузера

def get_settings_path():
    """
    Определяет путь к файлу настроек, учитывая, упаковано ли приложение.
    Логирует все важные события.
    """
    if getattr(sys, 'frozen', False):  # Проверка, запаковано ли приложение
        # Получаем домашнюю директорию пользователя для хранения настроек
        home_dir = Path.home()  # Определяем домашнюю директорию
        settings_dir = home_dir / '.TwixFlux'  # Пример директории для конфигурации
        settings_path = settings_dir / 'settings.json'  # Путь к файлу настроек

        # Логируем, что мы проверяем путь
        logger.info(f"Проверка настроек в упакованном приложении. Путь: {settings_path}")

        # Если файл настроек отсутствует, копируем его из ресурса
        if not settings_path.exists():
            # Путь к ресурсу в упакованном приложении
            packaged_settings_path = Path(sys._MEIPASS) / 'settings/settings.json'
            logger.info(f"Попытка копирования настроек из: {packaged_settings_path}")

            if packaged_settings_path.exists():  # Проверяем, существует ли файл настроек в упакованном приложении
                logger.info(f"Файл настроек найден в упакованном приложении. Копирование в: {settings_path}")
                settings_dir.mkdir(parents=True, exist_ok=True)  # Создаем директорию, если она не существует
                shutil.copy(packaged_settings_path, settings_path)  # Копируем файл настроек
                logger.info(f"Настройки успешно скопированы в {settings_path}")  # Логируем успешную копию
            else:
                logger.error("Файл настроек в упакованном приложении не найден.")  # Логируем ошибку
                raise FileNotFoundError("Файл настроек в упакованном приложении не найден.")  # Вызываем исключение
        else:
            logger.info(f"Файл настроек уже существует по пути: {settings_path}")  # Логируем, если файл уже существует
    else:
        # Если приложение не упаковано, используем обычный путь
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Получаем корень проекта
        settings_path = os.path.join(project_root, 'settings', 'settings.json')  # Формируем путь к файлу настроек
        logger.info(f"Используем обычный путь к настройкам: {settings_path}")  # Логируем путь к файлу настроек

    return settings_path  # Возвращаем путь к файлу настроек

def load_settings_by_category(category):
    """
    Извлекает настройки для указанной категории из файла settings.json.
    Логирует все шаги и выбрасывает ошибку, если категория отсутствует или файл недоступен.
    """
    try:
        settings_path = get_settings_path()  # Получаем путь к файлу настроек
        logger.info(f"🔄 Загрузка категории '{category}' из файла {settings_path}")  # Логируем начало загрузки категории

        with open(settings_path, "r") as json_file:  # Открываем файл настроек для чтения
            settings = json.load(json_file)  # Загружаем настройки из файла
            logger.info(f"Успешно загружены настройки из {settings_path}")  # Логируем успешную загрузку

        # Проверка наличия категории
        if category not in settings:  # Если категория не найдена в настройках
            error_message = f"Категория '{category}' отсутствует в файле настроек."  # Формируем сообщение об ошибке
            logger.error(f"❌ {error_message}")  # Логируем ошибку
            raise KeyError(error_message)  # Вызываем исключение KeyError

        return settings[category]  # Возвращаем настройки для указанной категории

    except FileNotFoundError:
        error_message = f"Файл настроек не найден по пути: {settings_path}"  # Формируем сообщение о несуществующем файле
        logger.error(f"❌ {error_message}")  # Логируем ошибку
        raise FileNotFoundError(error_message)  # Вызываем исключение FileNotFoundError
    except json.JSONDecodeError:
        error_message = "Файл настроек повреждён или имеет неверный формат."  # Формируем сообщение о неверном формате JSON
        logger.error(f"❌ {error_message}")  # Логируем ошибку
        raise json.JSONDecodeError(error_message, "", 0)  # Вызываем исключение JSONDecodeError
    except KeyError as e:  # Обработка ошибки, если категория не найдена
        logger.error(f"❌ {e}")  # Логируем ошибку
        raise  # Повторно вызываем ошибку
    except Exception as e:  # Обработка других непредвиденных ошибок
        logger.error(f"❌ Непредвиденная ошибка: {e}", exc_info=True)  # Логируем ошибку с информацией о стеке вызовов
        raise  # Вызываем исключение