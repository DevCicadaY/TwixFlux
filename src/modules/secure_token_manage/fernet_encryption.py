import sys  # Импортируем модуль для работы с системными параметрами
import os  # Импортируем модуль для работы с операционной системой
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))  # Добавляем родительскую директорию в путь поиска модулей
from src.utils.logger import logger  # Импортируем логгер для логирования действий

from cryptography.fernet import Fernet  # Импортируем класс Fernet для шифрования данных
import base64  # Импортируем модуль base64 для кодирования и декодирования данных
from settings.settings import load_settings_by_category, ENCRYPTION_CATEGORY  # Импортируем функцию для загрузки настроек и категорию настроек

# Глобальные переменные (Константы)
KEY_SIZE = None  # Размер ключа для Fernet (фиксированное значение для Fernet)
DEFAULT_KEY = None  # Настроенный ключ по умолчанию
ENCODING = None  # Кодировка данных

try:
    auth_settings = load_settings_by_category(ENCRYPTION_CATEGORY)  # Загружаем настройки из указанной категории
    logger.info(f"🔑 Получаем настройки 'ENCRYPTION_CATEGORY'...")  # Логируем информацию о загрузке настроек

    # Присваиваем настройки переменным
    KEY_SIZE = auth_settings.get("KEY_SIZE")  # Получаем размер ключа
    DEFAULT_KEY = auth_settings.get("DEFAULT_KEY")  # Получаем ключ по умолчанию
    ENCODING = auth_settings.get("ENCODING")  # Получаем кодировку данных

    # Выводим настройки в логи
    logger.info(f"🔑 KEY_SIZE: {KEY_SIZE}")  # Логируем размер ключа
    logger.info(f"🌐 DEFAULT_KEY: {DEFAULT_KEY}")  # Логируем ключ
    logger.info(f"🌐 ENCODING: {ENCODING}")  # Логируем кодировку

except Exception as e:  # Обрабатываем ошибку, если не удалось загрузить настройки
    logger.error(f"⚠️ Ошибка загрузки настроек 'ENCRYPTION_CATEGORY': {e}", exc_info=True)  # Логируем ошибку

# Генерация ключа для шифрования
def generate_key():  # Функция для генерации ключа для шифрования
    """Генерирует ключ для шифрования"""
    try:
        logger.info("🔑 Начинаем генерацию ключа для шифрования...")  # Логируем начало процесса генерации ключа
        key = Fernet.generate_key()  # Генерируем ключ для шифрования
        logger.info(f"🔑 Ключ для шифрования успешно сгенерирован: {key.decode()}")  # Логируем успешную генерацию ключа
        return key  # Возвращаем сгенерированный ключ
    except Exception as e:  # Обрабатываем ошибку, если генерация ключа не удалась
        logger.error(f"❌ Ошибка при генерации ключа: {e}", exc_info=True)  # Логируем ошибку
        return None  # Возвращаем None в случае ошибки

# Шифрование данных
def encrypt_data(data, key, encoding):  # Функция для шифрования данных
    """Шифрует данные с использованием Fernet"""
    try:
        logger.info(f"🔒 Начинаем шифрование данных...")  # Логируем начало процесса шифрования
        # Проверка длины ключа. Если длина ключа не 32 байта, генерируем новый
        decoded_key = base64.urlsafe_b64decode(key)  # Декодируем ключ из base64
        if len(decoded_key) != KEY_SIZE:  # Если длина ключа не соответствует заданному размеру, выбрасываем ошибку
            raise ValueError(f"Ключ должен быть длиной 32 байта, текущая длина: {len(decoded_key)}")

        fernet = Fernet(key)  # Создаем объект Fernet для работы с ключом
        encrypted_data = fernet.encrypt(data.encode(encoding))  # Шифруем данные с использованием кодировки
        logger.info("✅ Данные успешно зашифрованы.")  # Логируем успешное шифрование
        return encrypted_data  # Возвращаем зашифрованные данные
    except Exception as e:  # Обрабатываем ошибку при шифровании данных
        logger.error(f"❌ Ошибка при шифровании данных: {e}", exc_info=True)  # Логируем ошибку
        return None  # Возвращаем None в случае ошибки

# Расшифровка данных
def decrypt_data(encrypted_data, key, encoding):  # Функция для расшифровки данных
    """Расшифровывает данные с использованием Fernet"""
    try:
        logger.info(f"🔓 Начинаем расшифровку данных...")  # Логируем начало процесса расшифровки
        # Проверка длины ключа. Если длина ключа не 32 байта, генерируем новый
        decoded_key = base64.urlsafe_b64decode(key)  # Декодируем ключ из base64
        if len(decoded_key) != KEY_SIZE:  # Если длина ключа не соответствует заданному размеру, выбрасываем ошибку
            raise ValueError(f"Ключ должен быть длиной 32 байта, текущая длина: {len(decoded_key)}")

        fernet = Fernet(key)  # Создаем объект Fernet для работы с ключом
        decrypted_data = fernet.decrypt(encrypted_data).decode(encoding)  # Расшифровываем данные и декодируем их с использованием кодировки
        logger.info("✅ Данные успешно расшифрованы.")  # Логируем успешную расшифровку
        return decrypted_data  # Возвращаем расшифрованные данные
    except Exception as e:  # Обрабатываем ошибку при расшифровке данных
        logger.error(f"❌ Ошибка при расшифровке данных: {e}", exc_info=True)  # Логируем ошибку
        return None  # Возвращаем None в случае ошибки

# Проверка и получение ключа
def get_encryption_key():  # Функция для получения ключа шифрования
    global DEFAULT_KEY, KEY_SIZE  # Используем глобальные переменные DEFAULT_KEY и KEY_SIZE
    
    # Проверяем, существует ли уже ключ
    logger.info("🔑 Проверяем наличие ключа для шифрования...")  # Логируем начало проверки наличия ключа
    if DEFAULT_KEY is None:  # Если ключ не задан
        logger.info("DEFAULT_KEY не существует, генерируем новый... 🔑")  # Логируем информацию о том, что ключ будет сгенерирован
        DEFAULT_KEY = generate_key()  # Генерируем новый ключ для шифрования
    
    # Проверка формата ключа
    try:
        # Проверяем, является ли ключ корректным
        decoded_key = base64.urlsafe_b64decode(DEFAULT_KEY)  # Декодируем ключ из base64
        if len(decoded_key) != KEY_SIZE:  # Если длина ключа не соответствует заданному размеру
            logger.info("Ключ некорректен. Генерируем новый... 🔄")  # Логируем информацию о том, что ключ некорректен
            DEFAULT_KEY = generate_key()  # Генерируем новый ключ
            decoded_key = base64.urlsafe_b64decode(DEFAULT_KEY)  # Пересчитываем ключ после генерации нового
    except Exception as e:  # Обрабатываем ошибку при проверке ключа
        logger.error(f"Ошибка при проверке ключа: {e}. Генерируем новый ключ... 🔄", exc_info=True)  # Логируем ошибку
        DEFAULT_KEY = generate_key()  # Генерируем новый ключ
        decoded_key = base64.urlsafe_b64decode(DEFAULT_KEY)  # Пересчитываем ключ после генерации нового

    # Если KEY_SIZE задан, проверяем размер ключа
    if KEY_SIZE:
        if len(decoded_key) != KEY_SIZE:  # Если длина ключа не соответствует заданному размеру
            logger.info(f"Размер ключа должен быть {KEY_SIZE} байт. Генерируем новый ключ... 🔑")  # Логируем информацию о неправильном размере ключа
            DEFAULT_KEY = generate_key()  # Генерируем новый ключ
            decoded_key = base64.urlsafe_b64decode(DEFAULT_KEY)  # Пересчитываем ключ после генерации нового
    return DEFAULT_KEY  # Возвращаем текущий ключ

# Функция для шифрования данных
def encrypt_and_get_encrypted_data(data):  # Функция для шифрования данных и получения зашифрованных данных
    try:
        logger.info("🔒 Начинаем процесс шифрования данных...")  # Логируем начало процесса шифрования данных
        
        # Генерация ключа для шифрования
        key = get_encryption_key()  # Получаем ключ для шифрования

        if key:  # Если ключ получен
            # Шифрование данных
            encoding = ENCODING or 'utf-8'  # Используем заданную кодировку или по умолчанию utf-8
            encrypted_data = encrypt_data(data, key, encoding)  # Шифруем данные

            if encrypted_data:  # Если шифрование прошло успешно
                # Преобразуем зашифрованные данные в строку (без префикса b'')
                encrypted_data_str = encrypted_data.decode(encoding)  # Преобразуем зашифрованные данные в строку
                logger.info(f"Зашифрованные данные: {encrypted_data_str}")  # Логируем зашифрованные данные
                logger.info("✅ Процесс шифрования завершен успешно.")  # Логируем успешное завершение процесса
                return encrypted_data_str  # Возвращаем зашифрованные данные
            else:
                logger.error("❌ Ошибка при шифровании данных.")  # Логируем ошибку в случае неудачи
        else:
            logger.error("❌ Не удалось сгенерировать ключ для шифрования.")  # Логируем ошибку, если не удалось получить ключ
    except Exception as e:  # Обрабатываем общую ошибку
        logger.error(f"❌ Ошибка в процессе шифрования: {e}", exc_info=True)  # Логируем ошибку

# Функция для расшифровки данных
def decrypt_and_get_decrypted_data(encrypted_data):  # Функция для расшифровки данных
    try:
        logger.info("🔓 Начинаем процесс расшифровки данных...")  # Логируем начало процесса расшифровки данных
        
        # Генерация ключа для шифрования
        logger.info("Начинаем генерацию ключа для шифрования...")  # Логируем начало генерации ключа
        key = get_encryption_key()  # Получаем ключ для шифрования
        logger.info(f"Сгенерирован ключ для шифрования: {key}")  # Логируем полученный ключ

        if key:  # Если ключ получен
            # Расшифровка данных
            encoding = ENCODING or 'utf-8'  # Используем заданную кодировку или по умолчанию utf-8
            decrypted_data = decrypt_data(encrypted_data, key, encoding)  # Расшифровываем данные
            
            if decrypted_data:  # Если расшифровка прошла успешно
                logger.info("✅ Процесс расшифровки завершен успешно.")  # Логируем успешное завершение процесса
                return decrypted_data  # Возвращаем расшифрованные данные
            else:
                logger.error("❌ Ошибка при расшифровке данных.")  # Логируем ошибку в случае неудачи
        else:
            logger.error("❌ Не удалось сгенерировать ключ для шифрования.")  # Логируем ошибку, если не удалось получить ключ
    except Exception as e:  # Обрабатываем общую ошибку
        logger.error(f"❌ Ошибка в процессе расшифровки: {e}", exc_info=True)  # Логируем ошибку