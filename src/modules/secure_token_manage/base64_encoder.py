import sys  # Импортируем модуль sys для работы с системными параметрами и путями.
import os  # Импортируем модуль os для работы с операционной системой, например, для получения путей.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))  # Добавляем в путь директории путь на уровень выше для импорта.
from src.utils.logger import logger  # Импортируем объект logger из модуля, отвечающего за логирование.

import base64  # Импортируем модуль base64 для кодирования и декодирования в формат base64.
import re  # Импортируем модуль re для работы с регулярными выражениями (хотя он не используется в этом коде).

def encode_key_and_token(key: str, encrypted_token) -> str:
    """
    Объединяет ключ и зашифрованный токен, а затем кодирует их в base64.
    
    :param key: Ключ для шифрования.
    :param encrypted_token: Зашифрованный токен, который может быть строкой или байтами.
    :return: Закодированная строка в формате base64.
    """
    # Если encrypted_token является строкой, преобразуем её в байты
    if isinstance(encrypted_token, str):
        encrypted_token = encrypted_token.encode('utf-8')  # Преобразуем строку в байты, используя кодировку UTF-8.
    
    # Убедитесь, что encrypted_token теперь является байтами
    if not isinstance(encrypted_token, bytes):
        raise TypeError("encrypted_token должен быть объектом bytes")  # Проверяем тип переменной, она должна быть в байтовом формате.

    logger.info("🔐 Кодируем ключ и зашифрованный токен в base64...")  # Логируем начало процесса кодирования.

    # Кодируем ключ и токен в base64
    encoded_key = base64.b64encode(key.encode('utf-8')).decode('utf-8')  # Кодируем ключ в base64 и преобразуем в строку.
    encoded_token = base64.b64encode(encrypted_token).decode('utf-8')  # Кодируем токен в base64 и преобразуем в строку.
    
    # Объединяем закодированные данные
    combined_data = f"{encoded_key}|{encoded_token}"  # Формируем строку с двумя закодированными данными, разделенными '|'.
    logger.info(f"🎉 Закодированные данные в base64: {combined_data}")  # Логируем результат.
    return combined_data  # Возвращаем закодированные данные.

def decode_base64(encoded_data: str) -> bytes:
    """
    Декодирует строку из base64 в байты.
    
    :param encoded_data: Строка в формате base64.
    :return: Декодированные байты.
    """
    try:
        return base64.b64decode(encoded_data)  # Декодируем строку из base64 в байты.
    except Exception as e:
        logger.error(f"⚠️ Ошибка при декодировании base64: {str(e)}")  # Логируем ошибку, если она возникла.
        return None  # Возвращаем None, если произошла ошибка.

def decode_key_and_token(encoded_data: str):
    """
    Декодирует строку, содержащую закодированные ключ и токен, разделенные '|'.
    
    :param encoded_data: Строка, содержащая закодированные данные в формате base64.
    :return: Ключ и зашифрованный токен.
    """
    logger.info("🔓 Начинаем декодирование данных из base64...")  # Логируем начало процесса декодирования.
    
    try:
        # Разделяем строку на ключ и зашифрованный токен
        parts = encoded_data.split('|')  # Разделяем строку по символу '|' на две части.
        logger.info(f"📑 Разделенные данные: {parts}")  # Логируем результат разделения.

        if len(parts) != 2:
            logger.error(f"❌ Ошибка: Неверное количество частей после разделения. Ожидаются ключ и токен. Получено: {len(parts)}")
            return None, None  # Если данных не два, логируем ошибку и возвращаем None.

        # Декодируем каждый компонент из base64
        decoded_key = base64.b64decode(parts[0]).decode('utf-8')  # Декодируем ключ из base64.
        decoded_token = decode_base64(parts[1])  # Декодируем токен, используя функцию decode_base64.
        
        if decoded_token is None:
            logger.error("❌ Ошибка при декодировании токена.")  # Логируем ошибку, если токен не удалось декодировать.
            return None, None  # Возвращаем None, если токен не был декодирован.
        
        logger.info(f"🔑 Декодированный ключ: {decoded_key}")  # Логируем декодированный ключ.
        
        # Декодируем токен, чтобы избавиться от b'...'
        decoded_token_str = decoded_token.decode('utf-8') if isinstance(decoded_token, bytes) else decoded_token  # Преобразуем байты в строку, если токен был в байтовом формате.
        logger.info(f"🎟️ Декодированный токен: {decoded_token_str}")  # Логируем декодированный токен.

        return decoded_key, decoded_token_str  # Возвращаем декодированный ключ и токен.
    
    except Exception as e:
        logger.error(f"❌ Ошибка при декодировании данных: {str(e)}")  # Логируем ошибку при декодировании.
        return None, None  # Возвращаем None, если произошла ошибка при декодировании данных.