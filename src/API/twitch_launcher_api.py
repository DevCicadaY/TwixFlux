import time  # Для работы с задержками и временем
import psutil  # Для работы с процессами системы (например, для мониторинга процессов)
import os  # Для работы с операционной системой, например, манипуляции с файлами и путями
import sys  # Для доступа к аргументам командной строки и других системных функций
from fastapi import FastAPI, HTTPException  # FastAPI для создания веб-приложений и HTTPException для обработки ошибок
from fastapi.middleware.cors import CORSMiddleware  # CORS middleware для настройки разрешений на доступ к API с других доменов
from fastapi.responses import HTMLResponse  # Для отправки HTML-страниц в ответе на запросы
from fastapi.responses import FileResponse  # Для отправки файлов в ответах API
from threading import Thread  # Для выполнения задач в отдельных потоках (например, фоновые процессы)
from src.core.retry_launcher import retry_twitch_main  # Главная функция для повторного запуска процесса Twitch
from src.modules.browser.browser_launcher import quit_browser  # Функция для завершения работы с браузером
from src.utils.logger import logger  # Логгер для записи логов в файл или консоль
from src.utils import global_vars  # Глобальные переменные для хранения состояния приложения
from src.utils.terminate_process import terminate_processes  # Функция для завершения процессов, например, зависших
from src.modules.twitch.settings_twitch import get_stream_url, update_stream_url  # Функции для работы с URL стрима
from pydantic import BaseModel  # Pydantic для создания моделей данных для проверки и валидации данных
from src.modules.twitch.auto_shutdown_timer import update_auto_shutdown_timer  # Функция для обновления таймера автоматического завершения
# Создаем экземпляр приложения FastAPI
app = FastAPI()

# Разрешаем CORS для всех доменов
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все домены для кросс-доменных запросов
    allow_credentials=True,  # Разрешаем отправку куки
    allow_methods=["*"],  # Разрешаем все HTTP-методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

# Определяем маршрут для главной страницы (GET-запрос)
@app.get("/", response_class=HTMLResponse)
async def index():
    """Главная страница API."""
    
    # Получаем абсолютный путь к корню проекта
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Формируем путь к файлу конфигурации index.html в папке 'API'
    settings_path = os.path.join(project_root, 'API', 'index.html')

    # Логируем путь к файлу для отслеживания
    logger.info(f"Путь к файлу index.html: {settings_path}")
    
    # Проверяем существование файла
    if not os.path.exists(settings_path):
        # Если файл не найден, предупреждаем в логе и возвращаем ошибку 404
        logger.warning(f"⚠️ Файл {settings_path} не найден для отображения.")
        return HTMLResponse(content="<h1>⚠️ Файл index.html не найден.</h1>", status_code=404)

    try:
        # Логируем успешный запуск главной страницы
        logger.info("Запуск главной страницы")

        # Возвращаем содержимое файла через HTTP, используя FileResponse
        logger.info(f"✅ Отправляем файл {settings_path} по HTTP.")
        return FileResponse(settings_path)  # Используем FileResponse для отдачи файла

    except Exception as e:
        # Логируем ошибку, если произошла ошибка при обработке страницы
        logger.error(f"❌ Ошибка при обработке главной страницы: {e}")
        return HTMLResponse(content="<h1>❌ Ошибка загрузки страницы.</h1>", status_code=500)

# Определяем маршрут для запуска функции Twitch (POST-запрос)
@app.post("/start_twitch")
async def start_twitch():
    try:
        # Логируем запуск функции в отдельном потоке
        logger.info("🔁 Запуск twitch_main в отдельном потоке.")
        
        # Запускаем функцию retry_twitch_main в отдельном потоке для асинхронного выполнения
        thread = Thread(target=retry_twitch_main, daemon=True)  # Создаем поток для запуска функции
        thread.start()  # Запускаем поток
        return {"status": "success", "message": "Twitch automation started. 🎮"}  # Возвращаем успешный ответ

    except Exception as e:
        # Логируем ошибку, если произошла ошибка при запуске Twitch
        logger.error(f"❌ Ошибка при запуске Twitch: {str(e)}")
        return {"status": "error", "message": f"Ошибка: {str(e)}. ❌"}  # Возвращаем ошибку

# Маршрут для получения информации о браузере (GET-запрос)
@app.get("/browser_info")
async def get_browser_info():
    try:
        # Извлекаем информацию о браузере из глобальных переменных
        browser_info = {
            "session_id": global_vars.session_id,  # Идентификатор сессии браузера
            "driver": str(global_vars.driver) if global_vars.driver else None,  # Строковое представление драйвера, если он существует
            "pid": global_vars.pid,  # Идентификатор процесса браузера
            "server_url": global_vars.server_url  # URL сервера
        }
        
        # Логируем информацию о браузере для отслеживания
        logger.info(f"🔍 Информация о браузере: {browser_info}")
        
        # Возвращаем информацию о браузере в формате JSON
        return {"status": "success", "browser_info": browser_info}  # Возвращаем информацию о браузере

    except Exception as e:
        # Логируем ошибку, если произошла ошибка при получении информации о браузере
        logger.error(f"❌ Ошибка при получении информации о браузере: {str(e)}")
        # Возвращаем ошибку с подробным сообщением
        return {"status": "error", "message": f"Ошибка: {str(e)}. ❌"}

# Маршрут для завершения работы браузера (POST-запрос)
@app.post("/stop_browser")
async def stop_browser():
    """
    Завершает работу браузера и связанный процесс, если session_id совпадает.
    """
    logger.info("🛑 Запрос на завершение браузера получен.")
    
    # Проверяем, запущен ли браузер (если session_id не установлен, значит, браузер не запущен)
    if global_vars.session_id is None:
        logger.error("⚠️ Браузер не запущен.")
        # Если браузер не запущен, возвращаем ошибку 400 (Bad Request)
        raise HTTPException(status_code=400, detail="Браузер не запущен. 💤")

    try:
        # Логируем проверку session_id перед закрытием браузера
        logger.info(f"Проверка session_id: {global_vars.session_id}")
        
        # Закрываем браузер с использованием функции quit_browser
        quit_browser(global_vars.driver)
        logger.info("✅ Браузер успешно закрыт.")
        
        # Если процесс браузера запущен, завершить его по pid
        if global_vars.pid:
            shutdown_browser_process(global_vars.pid)  # Завершаем процесс браузера
        # Очищаем глобальные переменные, связанные с браузером
        global_vars.session_id = None
        global_vars.driver = None
        global_vars.pid = None
        global_vars.server_url = None

        logger.info("✅ Браузер и процесс успешно завершены.")
        # Возвращаем успешный ответ
        return {"status": "success", "message": "Process and browser successfully completed. 🛑"}

    except Exception as e:
        # Логируем ошибку при закрытии браузера или завершении процесса
        logger.error(f"❌ Ошибка при закрытии браузера и процессе: {str(e)}")
        # Возвращаем ошибку сервера с кодом 500
        raise HTTPException(status_code=500, detail="Произошла ошибка на сервере. ❌")

# Маршрут для завершения всех процессов (POST-запрос)
@app.post("/terminate_processes")
async def terminate_processes_api():
    # Завершаем все процессы с помощью функции terminate_processes
    terminate_processes()
    # Логируем успешное завершение процессов
    logger.info("✅ Процессы завершены.")
    # Возвращаем успешный ответ
    return {"status": "success", "message": "Processes completed. 🔚"}

# Функция для завершения процесса браузера
def shutdown_browser_process(pid: int):
    """Функция для завершения процесса браузера и всех связанных с ним процессов."""
    try:
        # Находим процесс по PID
        process = psutil.Process(pid)
        
        # Завершаем все дочерние процессы
        for child in process.children(recursive=True):
            child.terminate()
        
        # Завершаем сам процесс
        process.terminate()
        
        # Ожидаем завершения
        process.wait()
        
        logger.info(f"✅ Процесс с PID {pid} и его дочерние процессы были успешно завершены.")
    except psutil.NoSuchProcess:
        logger.error(f"❌ Процесс с PID {pid} не найден.")
    except psutil.AccessDenied:
        logger.error(f"❌ Нет прав для завершения процесса с PID {pid}.")
    except Exception as e:
        logger.error(f"❌ Ошибка при завершении процесса с PID {pid}: {e}")

# Инициализируем текущего стримера с помощью функции get_stream_url()
current_streamer = get_stream_url()  # Пример начального значения

# Модель для запроса на изменение имени стримера
class StreamerRequest(BaseModel):
    streamer: str

# Обработчик для получения текущего стримера
@app.get("/get_streamer")
async def get_streamer():
    """
    Обработчик для получения текущего стримера.
    Извлекает имя стримера из текущего URL (удаляет https://www.twitch.tv/).
    """
    streamer_name = current_streamer.replace("https://www.twitch.tv/", "")
    return {"streamer": streamer_name}

# Обработчик для изменения имени стримера
@app.post("/change_streamer")
async def change_streamer(request: dict):
    """
    Обработчик для изменения имени стримера.
    Обновляет имя стримера и соответствующий URL.
    """
    new_streamer = request.get('streamer')  # Получаем имя стримера
    if not new_streamer:
        raise HTTPException(status_code=400, detail="Streamer name is required.")
    
    # Обновляем имя стримера
    global current_streamer
    current_streamer = new_streamer

    # Обновляем URL стримера в настройках
    new_url = f"https://www.twitch.tv/{new_streamer}"
    update_stream_url(new_url)  # Обновляем URL

    return {"status": "success", "message": f"Streamer changed to {new_streamer} and URL updated."}

# Модель для запроса изменения таймера
class ShutdownTimerRequest(BaseModel):
    time: int  # Параметр time будет использоваться для указания времени таймера в секундах

@app.get("/get_shutdown_timer")
async def get_shutdown_timer():
    """
    Обработчик для получения текущего значения таймера автоматического завершения.
    Загружает настройки браузера и извлекает значение для ключа "AUTO_SHUTDOWN_TIMER".
    """
    browser_settings = load_browser_settings()  # Загружаем настройки браузера
    if browser_settings is None:
        raise HTTPException(status_code=400, detail="Failed to load browser settings.")
    
    auto_shutdown_timer = browser_settings.get("AUTO_SHUTDOWN_TIMER", "Not set")  # Получаем текущий таймер или "Not set"
    return {"AUTO_SHUTDOWN_TIMER": auto_shutdown_timer}

@app.post("/change_shutdown_timer")
async def change_shutdown_timer(request: ShutdownTimerRequest):
    """
    Обработчик для изменения значения таймера автоматического завершения.
    Принимает новый таймер в секундах через POST-запрос и обновляет настройки.
    """
    new_time = request.time  # Получаем значение времени из тела запроса
    if new_time <= 0:
        raise HTTPException(status_code=400, detail="Timer must be a positive integer.")  # Проверка на корректность значения

    # Вызываем функцию для обновления таймера с новым значением
    update_auto_shutdown_timer(new_time)
    
    return {"status": "success", "message": f"Shutdown timer updated to {new_time} seconds."}

if __name__ == '__main__':
    import uvicorn  # Импортируем Uvicorn для запуска сервера
    logger.info("🚀 Запуск API-сервера с использованием Uvicorn.")  # Логирование запуска сервера
    uvicorn.run(app, host="127.0.0.1", port=8000)  # Запуск сервера на указанном хосте и порту