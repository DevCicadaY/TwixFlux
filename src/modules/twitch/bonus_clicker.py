import datetime  # Импортируем модуль для работы с датами и временем
import time  # Импортируем модуль для работы с временем (задержки и паузы)
import threading  # Импортируем модуль для работы с многозадачностью (потоки)
from selenium.webdriver.common.by import By  # Импортируем класс для указания метода поиска элементов
from selenium.webdriver.support.ui import WebDriverWait  # Импортируем класс для ожидания появления элементов
from selenium.webdriver.support import expected_conditions as EC  # Импортируем класс для условий ожидания
from src.utils.logger import logger  # Импортируем логгер для записи логов

def get_bonus(driver, timeout_minutes=10, sleep_time=30):  # Функция для получения бонусов с кнопки
    """
    Получение бонусов с кнопки в течение указанного времени.
    
    :param driver: Экземпляр Selenium WebDriver.
    :param timeout_minutes: Время ожидания в минутах (по умолчанию 10).
    :param sleep_time: Интервал между проверками в секундах (по умолчанию 30).
    """
    bonus_button_xpath = "//button[contains(@aria-label, 'Получить бонус')]"  # XPath кнопки получения бонуса
    end_time = datetime.datetime.now() + datetime.timedelta(minutes=timeout_minutes)  # Время окончания процесса

    logger.info(f"🔄 Начинаем процесс получения бонуса. Таймаут: {timeout_minutes} минут, задержка: {sleep_time} секунд.")  # Логируем начало процесса получения бонусов
    
    def bonus_thread():  # Вспомогательная функция для выполнения процесса в отдельном потоке
        try:
            while datetime.datetime.now() < end_time:  # Выполняем цикл до истечения времени таймаута
                # Проверка, работает ли браузер
                try:
                    driver.title  # Проверяем, доступна ли страница (если браузер не работает, это вызовет исключение)
                except Exception as e:
                    logger.error(f"🚨 Браузер не работает или был закрыт: {e}")  # Логируем ошибку, если браузер не работает
                    break  # Завершаем выполнение функции

                try:
                    bonus_button = WebDriverWait(driver, 10).until(  # Ожидаем, пока кнопка не станет доступной
                        EC.element_to_be_clickable((By.XPATH, bonus_button_xpath))  # Указываем путь к кнопке
                    )
                    bonus_button.click()  # Нажимаем на кнопку получения бонуса
                    logger.info("✅ Бонус успешно получен.")  # Логируем успешное получение бонуса
                except Exception as e:
                    logger.debug(f"🔍 Кнопка не найдена или не доступна: {e}")  # Логируем ошибку, если кнопка не найдена или не доступна
                
                # Логируем время перед каждой паузой
                logger.info(f"🕒 Ожидание {sleep_time} секунд до следующей проверки.")  # Логируем информацию о задержке
                time.sleep(sleep_time)  # Пауза перед следующей проверкой

            logger.info("⏳ Процесс получения бонусов завершен по таймауту.")  # Логируем завершение процесса по таймауту
        except Exception as e:  # Обрабатываем исключения, если что-то пошло не так
            logger.error(f"❌ Произошла ошибка при получении бонусов: {e}")  # Логируем ошибку

    # Запуск задачи в отдельном потоке
    bonus_thread_instance = threading.Thread(target=bonus_thread)  # Создаём поток для выполнения задачи
    bonus_thread_instance.start()  # Запускаем поток
    
    logger.info("🌀 Задача получения бонуса запущена в отдельном потоке.")  # Логируем запуск задачи в потоке
    
    def stop_bonus_thread():  # Функция для остановки потока получения бонуса
        """
        Остановка потока получения бонуса.
        """
        bonus_thread_instance.join(timeout=1)  # Ожидаем завершения потока с тайм-аутом
        if bonus_thread_instance.is_alive():  # Проверяем, жив ли поток
            logger.info("⚠️ Задача получения бонуса продолжает работать.")  # Логируем, если поток продолжает работать
        else:
            logger.info("✅ Задача получения бонуса завершена.")  # Логируем, если поток завершён
    
    return stop_bonus_thread  # Возвращаем функцию для остановки потока