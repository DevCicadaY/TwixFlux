import sys  # Импортируем модуль sys для работы с системными параметрами
import os  # Импортируем модуль os для работы с операционной системой и путями файлов

# Добавляем родительскую директорию в sys.path для импорта модулей из других папок проекта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from src.utils.logger import logger  # Импортируем логгер для ведения журнала

import subprocess  # Импортируем модуль subprocess для выполнения системных команд
import shlex  # Импортируем модуль shlex для безопасной обработки строк в командной строке
from src.modules.secure_token_manage.keychain_cleanup import delete_keychain_items  # Импортируем функцию для очистки данных из keychain

# Конфигурация и настройки
PROJECT_NAME = "TwixFlux"  # Название проекта
SERVICE = f"{PROJECT_NAME}"  # Название сервиса, которое будет использовано в командах
ACCOUNT = os.getenv("USER")  # Получаем имя пользователя из переменных окружения
PASSWORD = ""  # Переменная для пароля (пока пустая)

def manage_keychain(delete_keychain=False):  # Функция для управления ключами
    if delete_keychain:  # Если флаг delete_keychain установлен в True
        delete_keychain_items(PROJECT_NAME)  # Удаляем элементы из keychain

# Функция для добавления элемента в macOS keychain
def add_keychain_item(service: str, account: str, password: str) -> bool:
    """
    Добавляет элемент в macOS keychain для указанного сервиса с данными учетной записи и пароля.

    :param service: Название сервиса, для которого будет сохранен элемент.
    :param account: Учетная запись (например, имя пользователя или email).
    :param password: Пароль, который будет сохранен в keychain.
    :return: True, если элемент успешно добавлен, False в случае ошибки.
    """
    try:
        # Экранируем аргументы для безопасности, чтобы избежать командных инъекций
        service_escaped = shlex.quote(service)
        account_escaped = shlex.quote(account)
        password_escaped = shlex.quote(password)

        # Формируем команду для добавления элемента в keychain
        add_command = f"security add-generic-password -s {service_escaped} -a {account_escaped} -w {password_escaped}"

        # Запускаем команду через subprocess и захватываем вывод
        result = subprocess.run(add_command, shell=True, capture_output=True, text=True)

        # Проверяем, если команда выполнена без ошибок
        if result.returncode == 0:
            logger.info(f"✅ Элемент для сервиса {service} успешно добавлен в keychain.")  # Логгируем успешное добавление
            return True
        else:
            logger.error(f"❌ Ошибка при добавлении элемента для сервиса {service}: {result.stderr}")  # Логгируем ошибку
            return False
    except subprocess.CalledProcessError as e:  # Если возникла ошибка при выполнении команды
        logger.error(f"❌ Ошибка при выполнении команды {e.cmd}: {e.output}")  # Логгируем ошибку с командой
        return False
    except Exception as e:  # Логгируем любые другие исключения
        logger.error(f"❌ Ошибка при добавлении элемента в keychain: {e}")
        return False

# Функция для извлечения элемента из macOS keychain
def get_keychain_item(service: str) -> str:
    """
    Извлекает элемент из macOS keychain для указанного сервиса.

    :param service: Название сервиса, для которого будет извлечен элемент.
    :return: Пароль, если элемент найден, иначе пустая строка.
    """
    try:
        logger.info("🔑 Извлекаем закодированные данные из хранилища...")  # Логгируем начало извлечения данных
        # Формируем команду для извлечения пароля из keychain
        get_command = f"security find-generic-password -s {service} -w"

        # Логируем команду перед выполнением
        logger.debug(f"📝 Выполняем команду для извлечения пароля: {get_command}")

        # Запускаем команду через subprocess и захватываем вывод
        result = subprocess.run(get_command, shell=True, capture_output=True, text=True)

        # Проверяем, если команда выполнена без ошибок
        if result.returncode == 0:
            password = result.stdout.strip()  # Получаем результат и удаляем лишние пробелы
            logger.debug(f"📄 Стандартный вывод: {result.stdout}")  # Логгируем вывод
            logger.info(f"🔑 Извлечённые данные из хранилища: {password}")  # Логгируем извлеченный пароль
            logger.info(f"✅ Пароль для сервиса {service} успешно извлечен.")  # Логгируем успех
            return password
        elif "SecKeychainSearchCopyNext" in result.stderr:  # Если ошибка "не найдено"
            logger.debug(f"⚠️ Стандартная ошибка: {result.stderr}")  # Логгируем ошибку
            logger.info("❌ Не удалось извлечь данные из хранилища!")  # Логгируем сообщение о неудаче
            logger.warning(f"⚠️ Элемент для сервиса {service} не найден в Keychain.")  # Логгируем предупреждение
            return ""
        else:
            logger.error(f"❌ Ошибка при извлечении элемента для сервиса {service}: {result.stderr.strip()}")  # Логгируем другие ошибки
            return ""
    except subprocess.CalledProcessError as e:  # Если возникла ошибка при выполнении команды
        logger.error(f"❌ Ошибка при выполнении команды: {e.cmd}\nКод ошибки: {e.returncode}\nСообщение: {e.output}")  # Логгируем подробную ошибку
        return ""
    except FileNotFoundError as e:  # Если команда не найдена
        logger.error(f"❌ Команда не найдена: {e}")  # Логгируем ошибку
        return ""
    except Exception as e:  # Логгируем любые другие исключения
        logger.error(f"❌ Неизвестная ошибка при извлечении элемента из keychain: {e}")
        return ""