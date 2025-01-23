# Анализ и сбор зависимостей
a = Analysis(
    ['TwixFlux.py'],  # Основной скрипт проекта
    pathex=['/Users/sergeysokulsky/Desktop/TwixFlux'],  # Путь к проекту, где находится основной файл
    binaries=[],  # Здесь указываются бинарные файлы, если они есть
    # Убедитесь, что правильно добавляете директорию и файл для включения в сборку
    datas=[  # Добавляем необходимые данные и файлы, которые должны быть включены в сборку
        ('src', 'src'),  # Копируем папку 'src' в ту же директорию в сборке
        ('config/browser_launcher.json', 'config'),  # Копируем конфигурационный файл
        ('settings/settings.json', 'settings'),  # Копируем настройки
        ('settings/settings.py', 'settings'),  # Копируем настройки
        ('src/API/index.html', 'src/API/'),  # Копируем HTML файл
        ('src/utils/chromedriver/macOS/chromedriver', 'chromedriver'),  # Включаем chromedriver для работы с Selenium
        ('myenv/bin/uvicorn', 'uvicorn')  # Включаем uvicorn для работы с FastAPI
    ],
    hiddenimports=[  # Добавляем скрытые импорты для библиотек, которые могут быть использованы в проекте
        'asyncio',  # Библиотека для асинхронного программирования
        'uvicorn',  # Сервер ASGI для запуска FastAPI приложений
        'selenium',  # Библиотека для автоматизации браузера
        'selenium.webdriver',  # Модуль для работы с драйверами Selenium
        'selenium.webdriver.support.ui',  # Поддержка UI для WebDriver
        'selenium.webdriver.support.expected_conditions',  # Условия ожидания в WebDriver
        'selenium.webdriver.chrome',  # Поддержка работы с браузером Chrome
        'selenium.webdriver.chrome.service',  # Для управления сервисом ChromeDriver
        'browser_launcher',  # Подключаем модуль для управления браузером
        'fastapi',  # Фреймворк для создания веб-приложений
        'fastapi.middleware',  # Миддлвары для FastAPI
        'fastapi.middleware.cors',  # Подключение CORS миддлвара для работы с кросс-доменными запросами
        'selenium.webdriver.chrome.servicebrowser_launcher',  # Ошибка в импорте, проверьте корректность
    ],
    hookspath=[],  # Путь к пользовательским хукам, если они есть
    hooksconfig={},  # Конфигурация для хука
    runtime_hooks=[],  # Хуки для времени выполнения
    excludes=[],  # Исключаемые файлы или модули
    noarchive=False,  # Скрывать архивированные файлы или нет
    optimize=0,  # Уровень оптимизации (можно изменить для ускорения выполнения)
)

# Создание PYZ архива
pyz = PYZ(a.pure)  # Создаем архив PYZ для упаковки чистого кода Python

# Генерация EXE файла
exe = EXE(
    pyz,  # Передаем собранный PYZ архив
    a.scripts,  # Скрипты, которые будут выполнены
    a.binaries,  # Бинарные файлы для включения в сборку
    a.datas,  # Данные, которые должны быть включены в сборку
    [],  # Дополнительные параметры
    name='TwixFlux',  # Название итогового файла EXE
    debug=False,  # Отключение отладочного режима
    bootloader_ignore_signals=False,  # Не игнорировать сигналы при загрузке
    strip=False,  # Не удалять отладочную информацию
    upx=True,  # Используем UPX для сжатия итогового файла
    upx_exclude=[],  # Исключаемые файлы из сжатия UPX
    runtime_tmpdir=None,  # Директория для временных файлов при выполнении
    console=False,  # Не открывать консоль при запуске EXE (можно поставить True для отладки)
    disable_windowed_traceback=False,  # Отключить стек ошибок для оконных приложений
    argv_emulation=False,  # Эмуляция аргументов командной строки
    target_arch=None,  # Архитектура целевой платформы
    codesign_identity=None,  # Информация для подписи кода (если требуется)
    entitlements_file=None,  # Файл прав доступа для подписанного кода
    icon='pyinstaller/icon.ico'  # Путь к иконке
)