import json  # Импортируем модуль json для работы с JSON данными.
import os  # Импортируем модуль os для работы с операционной системой, путями и файлами.
from selenium import webdriver  # Импортируем webdriver для управления браузером через Selenium.
from src.utils import global_vars  # Импортируем глобальные переменные для хранения данных сессии и состояния браузера.
from selenium.webdriver.chrome.service import Service  # Импортируем сервис Chrome для управления процессом ChromeDriver.
from selenium.webdriver.chrome.options import Options  # Импортируем опции для настройки браузера.
from src.utils.logger import logger  # Импортируем логгер для логирования действий в программе.
from src.utils.config_loader import load_config  # Импортируем функцию для загрузки конфигурации из файла.

# Загружаем конфигурацию из файла для получения пути к драйверу
logger.info("🔄 Загружаем конфигурацию...")  # Логируем начало загрузки конфигурации.
config = load_config()  # Загружаем конфигурацию из файла.
logger.info(f"✅ Конфигурация загружена: {config}")  # Логируем успешную загрузку конфигурации.

# Получаем относительный путь к Chrome драйверу из конфигурации
chrome_driver_relative_path = config["chrome_driver_path"]  # Извлекаем путь к ChromeDriver из конфигурации.
logger.info(f"🔑 Относительный путь к драйверу: {chrome_driver_relative_path}")  # Логируем относительный путь к драйверу.

# Получаем абсолютный путь к корню проекта для формирования полного пути
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))  # Получаем абсолютный путь к корню проекта.
logger.info(f"📂 Абсолютный путь к корню проекта: {project_root}")  # Логируем абсолютный путь к корню проекта.

# Формируем полный путь к драйверу, убирая возможный ведущий слэш
chrome_driver_path1 = os.path.join(project_root, chrome_driver_relative_path.lstrip('/'))  # Формируем полный путь к ChromeDriver.
logger.info(f"🔧 Полный путь к Chrome драйверу: {chrome_driver_path1}")  # Логируем полный путь к драйверу.

# Настройка опций для браузера
def get_browser_options(browser_mode):
    logger.info(f"🛠️ Получаем опции браузера для режима: {'headless' if browser_mode else 'normal'}")  # Логируем, какой режим выбран для браузера.
    options = Options()  # Создаем объект для настроек браузера.
    options.add_argument("--no-sandbox")  # Отключаем песочницу для улучшения производительности.
    options.add_argument("--disable-dev-shm-usage")  # Отключаем использование разделяемой памяти.
    options.add_argument("--mute-audio")  # Отключаем звук в браузере.
    options.add_argument("--disable-extensions")  # Отключаем расширения браузера.
    
    if browser_mode:
        options.add_argument("--headless")  # Включаем режим без графического интерфейса (headless).
        options.add_argument("--disable-gpu")  # Отключаем аппаратное ускорение.
        options.add_argument("--remote-debugging-port=9222")  # Включаем порт для удаленной отладки.
    
    logger.info(f"✅ Настройки браузера: {options.arguments}")  # Логируем примененные настройки браузера.
    return options  # Возвращаем настройки браузера.

# Запуск браузера с нужными параметрами
def start_browser(chrome_driver_path, options):
    """
    Функция для запуска браузера, сохранения важных данных о сессии и логирования событий.
    """
    try:
        logger.info("🚀 Запуск браузера...")  # Логируем начало запуска браузера.
        service = Service(chrome_driver_path1)  # Создаем объект для управления сервисом ChromeDriver.
        driver = webdriver.Chrome(service=service, options=options)  # Запускаем браузер с указанным драйвером и настройками.
        
        logger.info("✅ Браузер успешно запущен.")  # Логируем успешный запуск браузера.

        # Извлекаем session_id с driver и сохраняем в глобальную переменную
        global_vars.session_id = driver.session_id  # Сохраняем session_id в глобальную переменную.
        logger.info(f"🎯 Session ID: {global_vars.session_id} - Браузер успешно запущен! 🚀")  # Логируем session_id.

        # Извлекаем driver и сохраняем в глобальную переменную
        global_vars.driver = driver  # Сохраняем объект driver в глобальную переменную.
        logger.info(f"🔑 Экстракция driver завершена: {global_vars.driver}")  # Логируем объект driver.

        # Извлекаем PID с driver и сохраняем в глобальную переменную
        global_vars.pid = driver.service.process.pid  # Получаем PID процесса браузера.
        logger.info(f"🔢 PID процесса браузера: {global_vars.pid}")  # Логируем PID процесса браузера.

        # Извлечение URL сервера WebDriver
        if driver.service:
            global_vars.server_url = driver.service.service_url  # Извлекаем URL сервера WebDriver.
            logger.info(f"🌐 URL сервера WebDriver: {global_vars.server_url}")  # Логируем URL сервера WebDriver.
        else:
            global_vars.server_url = None  # Если URL не был получен, устанавливаем его в None.
            logger.warning("⚠️ Не удалось извлечь WebDriver URL через service.")  # Логируем предупреждение.
            logger.info(f"🔍 Доступные возможности WebDriver: {driver.capabilities}")  # Логируем доступные возможности WebDriver.
        
        # Логируем обновление всех переменных для отладки
        logger.info(f"📊 Обновленные значения переменных: session_id={global_vars.session_id}, driver={global_vars.driver}, pid={global_vars.pid}, server_url={global_vars.server_url}")  # Логируем обновленные переменные.

        return driver  # Возвращаем объект driver для дальнейшего использования.
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске браузера: {e}")  # Логируем ошибку при запуске браузера.
        exit()  # Завершаем программу при возникновении ошибки.

# Закрытие браузера и сброс глобальных переменных
def quit_browser(driver):
    """
    Функция для закрытия браузера и сброса глобальных переменных.
    """
    if driver and hasattr(driver, "session_id") and driver.session_id:  # Проверяем, что браузер существует и имеет session_id.
        try:
            # Логируем попытку закрытия браузера
            session_id = driver.session_id  # Извлекаем session_id браузера.
            current_url = driver.current_url if hasattr(driver, "current_url") else "URL недоступен"  # Получаем текущий URL, если доступен.
            page_title = driver.title if hasattr(driver, "title") else "Заголовок недоступен"  # Получаем заголовок страницы, если доступен.
            
            logger.info(f"❌ Попытка закрытия браузера 🖥️: session_id={session_id}, URL={current_url}, title={page_title}")  # Логируем попытку закрытия браузера.
            driver.quit()  # Закрываем браузер.
            reset_global_vars()  # Сбрасываем глобальные переменные.
            logger.info("✅ Браузер успешно закрыт 🛑.")  # Логируем успешное закрытие браузера.
            return None  # Возвращаем None, чтобы сбросить объект driver.
        except Exception as e:
            logger.error(f"❌ Ошибка при закрытии браузера: {e}", exc_info=True)  # Логируем ошибку при закрытии браузера.
            return driver  # Возвращаем объект driver, если не удалось его закрыть.
    else:
        logger.info("💤 Браузер уже закрыт или не был запущен. 💤")  # Логируем, что браузер уже закрыт или не был запущен.
        return driver  # Возвращаем объект driver.

# Функция для сброса глобальных переменных, которые используются для управления браузером
def reset_global_vars():
    """
    Функция для очистки глобальных переменных, которые используются для управления браузером.
    """
    try:
        logger.info("🔄 Сброс глобальных переменных...")  # Логируем начало сброса глобальных переменных.

        # Сбрасываем значения глобальных переменных
        global_vars.session_id = None  # Сбрасываем session_id.
        global_vars.driver = None  # Сбрасываем driver.
        global_vars.pid = None  # Сбрасываем PID.
        global_vars.server_url = None  # Сбрасываем URL сервера WebDriver.

        logger.info("✅ Глобальные переменные успешно очищены!")  # Логируем успешное очищение глобальных переменных.
    except Exception as e:
        logger.error(f"❌ Ошибка при сбросе глобальных переменных: {e}")  # Логируем ошибку при сбросе глобальных переменных.