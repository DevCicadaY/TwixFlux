import sys  # Импортируем модуль sys для работы с системными параметрами и путями
import os  # Импортируем модуль os для работы с операционной системой и путями файлов

# Добавляем родительскую директорию в sys.path, чтобы импортировать модули из других папок
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Импортируем логгер для ведения журналов
from src.utils.logger import logger

# Импортируем функции для работы с токеном Twitch, шифрования, расшифровки, кодирования/декодирования, и хранилища ключей
from src.modules.secure_token_manage.twitch_token_extractor import get_twitch_auth_token  # Функция для получения токена Twitch
from src.modules.secure_token_manage.fernet_encryption import get_encryption_key, encrypt_and_get_encrypted_data, decrypt_and_get_decrypted_data, ENCODING  # Функции для генерации ключа, шифрования и расшифровки
from src.modules.secure_token_manage.base64_encoder import encode_key_and_token, decode_key_and_token  # Функции для кодирования/декодирования в base64
from src.modules.secure_token_manage.keychain_manager import PROJECT_NAME, SERVICE, ACCOUNT, manage_keychain, add_keychain_item, get_keychain_item  # Модуль для работы с хранилищем ключей

def main_function():  # Основная функция, которая выполняет процесс шифрования и работы с токеном
    global AUTH_TOKEN  # Объявляем переменную AUTH_TOKEN как глобальную для использования в других частях программы
    try:
        # Удаление старых данных из хранилища ключей для обновления информации
        manage_keychain(delete_keychain=True)  # 🧰 Удаление старых данных из хранилища ключей

        # 1. Генерация ключа для шифрования с помощью функции get_encryption_key
        # Этот ключ будет использоваться для шифрования токена Twitch
        key = get_encryption_key()  # Генерация ключа для шифрования
        logger.info("🔑 Генерация ключа для шифрования...")  # Логгирование сообщения о процессе генерации ключа

        # 2. Получение токена Twitch, используя функцию get_twitch_auth_token
        # Токен необходим для доступа к Twitch API
        data_to_encrypt = get_twitch_auth_token()  # Получение токена Twitch

        # Проверка, что токен был успешно получен
        if data_to_encrypt:  # Если токен получен
            logger.info(f"🎮✨ Полученный токен Twitch: {data_to_encrypt}")  # Логгирование полученного токена

            # 3. Шифрование данных
            # Токен шифруется для безопасного хранения и передачи
            encrypted = encrypt_and_get_encrypted_data(data_to_encrypt)  # Шифрование токена
            logger.info("🔒 Токен успешно зашифрован.")  # Логгирование сообщения о том, что токен был зашифрован

            # 4. Кодирование ключа и зашифрованного токена в base64
            # Это позволяет объединить ключ и зашифрованный токен в одну строку
            encoded_result = encode_key_and_token(key, encrypted)  # Кодирование ключа и зашифрованного токена в base64
            logger.info("🔐 Кодирование ключа и зашифрованного токена в base64...")  # Логгирование начала кодирования

            # 5. Сохраняем закодированные данные в хранилище ключей (Keychain)
            add_keychain_item(SERVICE, ACCOUNT, encoded_result)  # Сохранение закодированных данных в Keychain
            logger.info("✅ Данные успешно сохранены в хранилище ключей.")  # Логгирование успешного сохранения данных в хранилище

            # 6. Извлекаем закодированные данные из хранилища
            password = get_keychain_item(SERVICE)  # Извлечение данных из хранилища
            logger.info("🔑 Извлечение закодированных данных из хранилища...")  # Логгирование процесса извлечения данных

            # 7. Декодирование данных из base64 обратно в исходные компоненты (ключ и зашифрованный токен)
            encoded_data = password  # Получаем закодированные данные

            # Вызов функции для декодирования ключа и токена
            key, encrypted_token = decode_key_and_token(encoded_data)  # Декодирование данных
            logger.info(f"🗝  Ключ: {key}")  # Логгирование декодированного ключа
            logger.info(f"🔑 Зашифрованный токен: {encrypted_token}")  # Логгирование зашифрованного токена

            # 8. Расшифровка данных
            if encrypted_token:  # Если зашифрованный токен существует
                logger.info("🔓 Попытка расшифровать зашифрованные данные...")  # Логгирование попытки расшифровки
                decrypted_data = decrypt_and_get_decrypted_data(encrypted_token)  # Расшифровка зашифрованного токена
                logger.info(f"📜 Расшифрованные данные: {decrypted_data}")  # Логгирование расшифрованных данных
                AUTH_TOKEN = decrypted_data  # Присваивание расшифрованных данных переменной AUTH_TOKEN
                logger.info(f"📜 Результат расшифровки в новой переменной: {AUTH_TOKEN}")  # Логгирование результата расшифровки
            else:
                logger.warning("⚠️ Данные для расшифровки отсутствуют.")  # Логгирование предупреждения об отсутствии данных для расшифровки
        else:
            # Если токен не был получен, записываем сообщение об ошибке
            logger.error("❌ Не удалось получить токен Twitch. Проверьте соединение или параметры.")  # Логгирование ошибки

    except Exception as e:  # Обработка исключений, если что-то пошло не так
        logger.error(f"⚠️ Произошла ошибка: {e}")  # Логгирование ошибки

# Вызов основной функции
main_function()  # Запуск основной функции