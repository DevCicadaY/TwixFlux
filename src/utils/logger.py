import logging  # Импортируем модуль для логирования
import os  # Импортируем модуль для работы с операционной системой
import sys  # Импортируем модуль для работы с системой (например, завершение работы программы)
import signal  # Импортируем модуль для работы с сигналами
import threading  # Импортируем модуль для работы с потоками
from src.utils.clean_pycache import remove_pycache_in_project  # Импортируем функцию для очистки кэша Python

# Получаем путь к корню проекта
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))  # Определяем корневую директорию проекта

# Формируем путь к лог-файлу
log_file = os.path.join(project_root, 'logs', 'app.log')  # Создаем путь к лог-файлу внутри директории 'logs'

# Создаем папку для логов, если она не существует
os.makedirs(os.path.dirname(log_file), exist_ok=True)  # Если директория для логов не существует, она будет создана

# Формат логов
log_format = '[%(asctime)s] %(levelname)s - %(message)s'  # Определяем формат выводимых сообщений в логах
date_format = '%Y-%m-%d %H:%M'  # Определяем формат отображения времени в логах

# Переключатель для включения/выключения логирования
logging_enabled = os.getenv("LOGGING_ENABLED", "True") == "True"  # Получаем переменную окружения для включения/выключения логирования

# Функция для настройки логирования
def setup_logging():
    if logging_enabled:  # Если логирование включено
        # Если логирование включено, настраиваем обработчики для вывода логов
        logging.basicConfig(
            level=logging.INFO,  # Уровень логирования (INFO – сообщения об основной деятельности)
            format=log_format,  # Устанавливаем формат сообщений в логах
            datefmt=date_format,  # Устанавливаем формат времени в логах
            handlers=[
                logging.StreamHandler(),  # Выводим логи в консоль
                logging.FileHandler(log_file)  # Записываем логи в файл
            ]
        )
    else:  # Если логирование отключено
        # Если логирование выключено, устанавливаем минимальный уровень логирования
        logging.basicConfig(level=logging.CRITICAL)  # Записываем только критические ошибки

# Настройка логирования
setup_logging()  # Вызываем функцию настройки логирования

# Логгер для приложения
logger = logging.getLogger('app_logger')  # Создаем объект логгера с именем 'app_logger'

# Обработчик прерывания (Ctrl+C)
def handle_interrupt(signal, frame):
    logger.info("🚫 Процесс был прерван пользователем (Ctrl+C). Завершаем работу.")  # Логируем информацию о прерывании
    # Вызов функции для очистки pycache
    try:
        remove_pycache_in_project()  # Пытаемся очистить кэш Python
        logger.info("🧹 Кэш Python успешно очищен.")  # Логируем успешное очищение кэша
    except Exception as e:
        logger.error(f"❌ Ошибка при очистке кэша: {e}")  # Логируем ошибку, если она произошла
    
    # Завершаем программу
    logger.info("🚀 Программа завершает работу после очистки.")  # Логируем информацию о завершении работы программы
    sys.exit(0)  # Завершаем выполнение программы с кодом 0 (успех)

# Регистрация обработчика для сигнала Ctrl+C только в главном потоке
if threading.current_thread() is threading.main_thread():  # Проверяем, что это главный поток
    # Привязываем обработчик сигнала прерывания (Ctrl+C) к функции handle_interrupt
    signal.signal(signal.SIGINT, handle_interrupt)  # Устанавливаем обработчик для сигнала прерывания (Ctrl+C)