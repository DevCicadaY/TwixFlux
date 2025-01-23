import sys  # Импортируем модуль для работы с системой
import os  # Импортируем модуль для работы с операционной системой
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))  # Добавляем путь к родительской директории в sys.path для импорта модулей
from src.utils.logger import logger  # Импортируем логгер для логирования событий

# Импортируем функции для шифрования/расшифровки, кодирования/декодирования и работы с keychain
from src.modules.secure_token_manage.fernet_encryption import get_encryption_key, encrypt_and_get_encrypted_data, decrypt_and_get_decrypted_data, ENCODING
from src.modules.secure_token_manage.base64_encoder import encode_key_and_token, decode_key_and_token  # Функции для кодирования/декодирования в base64
from src.modules.secure_token_manage.keychain_manager import PROJECT_NAME, SERVICE, ACCOUNT, manage_keychain, get_keychain_item  # Модуль для работы с хранилищем ключей

if __name__ == "__main__":  # Точка входа в программу
    try:
        # Инициализация хранилища ключей без удаления текущих данных
        manage_keychain(delete_keychain=False)
        
        # Получаем пароль (или токен) из хранилища ключей
        password = get_keychain_item(SERVICE)

        # Если пароль не найден в хранилище, выводим ошибку и завершаем программу
        if password is None:
            logger.error("❌ Не удалось найти пароль в хранилище.")  # Логируем ошибку
            exit(1)  # Завершаем выполнение программы с кодом 1

        # Если пароль найден, выводим успешное сообщение
        logger.info("🔑 Пароль успешно извлечен из хранилища.")  # Логируем успешное извлечение пароля

        # Декодируем данные из base64 в их исходные компоненты (ключ и зашифрованный токен)
        encoded_data = password  # Присваиваем данные из хранилища переменной

        # Декодируем закодированные данные (ключ и токен) из base64
        logger.info("🔓 Декодирование данных из base64...")  # Логируем начало декодирования
        key, encrypted_token = decode_key_and_token(encoded_data)  # Декодируем данные

        # Логируем ключ и зашифрованный токен для последующего использования
        logger.info(f"🔑 Ключ: {key}")  # Логируем ключ
        logger.info(f"🔐 Зашифрованный токен: {encrypted_token}")  # Логируем зашифрованный токен
        
        # Проверяем, если зашифрованный токен существует, пытаемся его расшифровать
        if encrypted_token:
            logger.info("🔑 Попытка расшифровать зашифрованные данные...")  # Логируем начало расшифровки
            decrypted_data = decrypt_and_get_decrypted_data(encrypted_token)  # Расшифровываем данные
            # Логируем расшифрованные данные
            logger.info(f"📜 Расшифрованные данные: {decrypted_data}")
        else:
            # Если данные для расшифровки отсутствуют, выводим предупреждение
            logger.warning("⚠️ Данные для расшифровки отсутствуют.")  # Логируем предупреждение

    except Exception as e:  # Обрабатываем любые исключения
        # Логируем ошибку, если что-то пошло не так
        logger.error(f"⚠️ Произошла ошибка: {e}")  # Логируем ошибку