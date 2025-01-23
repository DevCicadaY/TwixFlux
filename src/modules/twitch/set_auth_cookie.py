from src.modules.browser.browser_launcher import load_config  # Импорт функции для загрузки конфигурации браузера
from src.utils.logger import logger  # Импорт логгера для записи логов

from src.modules.secure_token_manage.token_storage_manager import AUTH_TOKEN  # Импорт переменной AUTH_TOKEN для установки в cookie

AUTH_TOKEN  # Получаем переменную с авторизационным токеном

# Установка cookies
def set_auth_cookie(driver, AUTH_TOKEN):
    try:
        logger.info("🌐 Переход на сайт Twitch...")  # Логируем информацию о переходе на сайт Twitch
        driver.get("https://www.twitch.tv")  # Переходим на сайт Twitch
        logger.info("✅ Установка auth-token в cookies...")  # Логируем информацию о установке токена в cookies
        
        # Логирование параметров cookie
        logger.debug(f"🍪 Устанавливаем cookie: auth-token={AUTH_TOKEN}, domain=.twitch.tv, path=/")  # Логируем параметры cookie
        
        driver.add_cookie({
            "name": "auth-token",  # Устанавливаем имя cookie
            "value": AUTH_TOKEN,  # Устанавливаем значение cookie как auth-token
            "domain": ".twitch.tv",  # Указываем домен для cookie
            "path": "/",  # Указываем путь для cookie
        })
        
        # Логируем успешную установку cookie
        logger.info("🍪 auth-token успешно добавлен в cookies.")  # Логируем успешное добавление токена в cookies
        
        driver.refresh()  # Обновляем страницу
        logger.info("🔄 Сайт Twitch обновлен, auth-token применен.")  # Логируем успешное обновление страницы
        
        # Логируем текущий URL после обновления страницы
        current_url = driver.current_url  # Получаем текущий URL страницы
        logger.info(f"🌍 Текущий URL после обновления: {current_url}")  # Логируем текущий URL

    except Exception as e:  # Обрабатываем исключения, если что-то пошло не так
        logger.error(f"❌ Ошибка при добавлении cookie или обновлении страницы: {e}", exc_info=True)  # Логируем ошибку

        # Логируем текущий URL и состояние драйвера перед завершением
        if hasattr(driver, 'current_url'):  # Проверяем, есть ли атрибут current_url у драйвера
            current_url = driver.current_url  # Получаем текущий URL
            logger.info(f"🌍 Текущий URL на момент ошибки: {current_url}")  # Логируем текущий URL на момент ошибки

        driver.quit()  # Закрытие браузера
        logger.info("🚨 Браузер закрыт из-за ошибки.")  # Логируем информацию о закрытии браузера
        
        exit()  # Завершаем выполнение программы, если произошла ошибка