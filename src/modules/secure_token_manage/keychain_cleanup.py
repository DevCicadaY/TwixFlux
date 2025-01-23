import sys  # Импортируем модуль для работы с системой
import os  # Импортируем модуль для работы с операционной системой
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))  # Добавляем путь к родительской директории в sys.path для импорта модулей
from src.utils.logger import logger  # Импортируем логгер для логирования событий

import subprocess  # Импортируем модуль для работы с процессами

# Название проекта
PROJECT_NAME = "TwixFlux"  # Указываем название проекта, которое будет использоваться в ключах

# Поиск и удаление всех элементов из keychain, связанных с указанным сервисом
def delete_keychain_items(service: str) -> bool:
    """
    Ищет и удаляет все элементы с указанным названием сервиса из keychain.

    :param service: Название сервиса (например, "MyApp").
                    Используется для поиска и удаления соответствующих элементов из keychain.
    :return: True, если все элементы были удалены, False в случае ошибки или если элементы не были найдены.
    """
    try:
        logger.info("🔑 Сохраняем закодированные данные в хранилище ключей...")  # Логируем начало процесса
        # Формируем команду для поиска всех элементов в keychain по имени сервиса
        find_command = f"security find-generic-password -s {service}"

        # Запускаем команду через subprocess. Получаем вывод и ошибки.
        result = subprocess.run(find_command, shell=True, capture_output=True, text=True)

        # Если команда завершилась успешно (возвращает код 0), значит, есть хотя бы один элемент с таким сервисом.
        if result.returncode == 0:
            logger.info(f"🔍 Элементы с сервисом {service} найдены. Начинаем удаление...")  # Логируем, что элементы найдены и начинается их удаление

            # Формируем команду для удаления элементов с данным сервисом
            delete_command = f"security delete-generic-password -s {service}"
            while True:
                # Пытаемся удалить каждый элемент
                subprocess.run(delete_command, shell=True)

                # Проверяем, остались ли еще элементы с таким сервисом в keychain
                result = subprocess.run(find_command, shell=True, capture_output=True, text=True)
                if result.returncode != 0:
                    break  # Если больше нет элементов, выходим из цикла

            logger.info(f"✅ Все элементы с сервисом {service} удалены.")  # Логируем успешное удаление
            return True  # Возвращаем True, если все элементы удалены
        else:
            logger.warning(f"⚠️ Элементы с сервисом {service} не найдены в keychain.")  # Логируем, что элементы не были найдены
            return False  # Возвращаем False, если элементы не найдены
    except subprocess.CalledProcessError as e:
        # Обработка ошибок, если команда завершилась с ошибкой
        logger.error(f"❌ Ошибка при выполнении команды {e.cmd}: {e.output}")  # Логируем ошибку
        return False  # Возвращаем False при возникновении ошибки
    except Exception as e:
        # Обработка остальных ошибок
        logger.error(f"❌ Ошибка при удалении элементов из keychain: {e}")  # Логируем общую ошибку
        return False  # Возвращаем False при возникновении ошибки