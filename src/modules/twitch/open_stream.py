from selenium.webdriver.common.by import By  # Импортируем класс для указания метода поиска элементов
from selenium.webdriver.support.ui import WebDriverWait  # Импортируем класс для ожидания появления элементов
from selenium.webdriver.support import expected_conditions as EC  # Импортируем класс для условий ожидания
from src.modules.browser.browser_launcher import load_config  # Импортируем функцию для загрузки конфигурации браузера
from src.utils.logger import logger  # Импортируем логгер для записи логов

# Открытие стрима
def open_stream(driver, stream_url):  # Функция для открытия стрима по указанному URL
    try:
        logger.info(f"🌐 Переход на стрим: {stream_url}")  # Логируем информацию о переходе на стрим
        driver.get(stream_url)  # Переходим на страницу стрима по URL
        logger.info(f"⏳ Ожидание загрузки видео на странице: {stream_url}...")  # Логируем ожидание загрузки видео

        # Ожидание загрузки элемента video
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "video")))  # Ожидаем появления элемента video на странице
        logger.info(f"✅ Видео элемент найден на стриме: {stream_url}")  # Логируем успешное нахождение видео элемента
        
        logger.info("🎥 Стрим успешно открыт.")  # Логируем успешное открытие стрима
        
        # Логируем текущий URL после открытия стрима
        current_url = driver.current_url  # Получаем текущий URL страницы
        logger.info(f"🌍 Текущий URL после открытия стрима: {current_url}")  # Логируем текущий URL

    except Exception as e:  # Обрабатываем исключения, если что-то пошло не так
        logger.error(f"❌ Ошибка при открытии стрима: {e}", exc_info=True)  # Логируем ошибку и стек вызовов

        # Логируем текущий URL и состояние драйвера перед завершением
        if hasattr(driver, 'current_url'):  # Проверяем, есть ли атрибут current_url у драйвера
            current_url = driver.current_url  # Получаем текущий URL
            logger.info(f"🌍 Текущий URL на момент ошибки: {current_url}")  # Логируем текущий URL на момент ошибки

        driver.quit()  # Закрытие браузера
        logger.info("🚨 Браузер закрыт из-за ошибки.")  # Логируем информацию о закрытии браузера из-за ошибки
        
        exit()  # Завершаем выполнение программы, если произошла ошибка