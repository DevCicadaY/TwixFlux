import subprocess  # Импортируем модуль для работы с процессами через системные команды
import os  # Импортируем модуль для работы с операционной системой
import signal  # Импортируем модуль для работы с сигналами операционной системы
from src.utils.logger import logger  # Импортируем логгер для записи сообщений
from src.modules.browser.browser_launcher import quit_browser, reset_global_vars  # Импортируем функции для работы с браузером (закрытие и сброс переменных)
from src.utils import global_vars  # Импортируем глобальные переменные

def find_process_by_name(process_name):
    """Ищем процессы по имени через pgrep"""
    try:
        # Выполняем команду pgrep с флагом -f для поиска всех процессов по имени
        result = subprocess.check_output(["pgrep", "-f", process_name]).decode("utf-8")  # Получаем результат в виде строки
        # Разбиваем строку на строки и конвертируем их в список целых чисел (PID)
        return [int(pid) for pid in result.splitlines()]
    except subprocess.CalledProcessError:
        # Если pgrep не нашел процессы, возвращаем пустой список
        return []

def terminate_processes():
    """Завершаем все процессы с именами process_name_1 и process_name_2"""
    # Список процессов, которые необходимо завершить
    process_names = ["TwixFlux", "Python"]  # Имена процессов, которые мы ищем и завершаем
    
    # Проходим по каждому имени процесса из списка
    for process_name in process_names:
        # Ищем процессы с данным именем с помощью функции find_process_by_name
        pids = find_process_by_name(process_name)
        
        # Если процессы найдены
        if pids:
            # Логируем информацию о найденных процессах и их PID
            logger.info(f"✅ Найдены процессы {process_name}: {pids}")
            
            # Для каждого PID из найденных процессов
            for pid in pids:
                # Логируем информацию о процессе, который будем завершать
                logger.info(f"🛑 Завершаем процесс с PID: {pid}")
                # Отправляем процессу сигнал завершения (SIGTERM)
                os.kill(pid, signal.SIGTERM)  # Завершаем процесс с указанным PID
                # Логируем успешное завершение процесса
                logger.info(f"✅ Процесс с PID {pid} успешно завершен.")
        else:
            # Если процессы с данным именем не найдены, логируем предупреждение
            logger.warning(f"⚠️ Процесс {process_name} не найден.")

if __name__ == "__main__":  # Главная точка входа в программу
    driver = None  # Инициализируем переменную driver для WebDriver (если используется в проекте)
    
    # Закрываем браузер, если WebDriver был инициализирован
    quit_browser(driver)  # Вызов функции для закрытия браузера
    
    # Сбрасываем глобальные переменные, чтобы очистить настройки и состояния
    reset_global_vars()  # Вызов функции для сброса глобальных переменных
    
    # Завершаем процессы с именами "TwixFlux" и "Python"
    terminate_processes()  # Вызов функции для завершения процессов