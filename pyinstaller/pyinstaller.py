import os  # Модуль для работы с файловой системой: проверка существования файлов и директорий, удаление файлов и папок.
import sys  # Модуль для работы с аргументами командной строки и взаимодействия с системой.
import shutil  # Модуль для работы с файлами и папками: копирование, удаление целых директорий.
import subprocess  # Модуль для выполнения системных команд и процессов через Python.
from src.utils.logger import logger  # Пользовательский логгер для ведения логов, выводит информацию и ошибки.

# Пути к файлам
spec_file = 'pyinstaller/TwixFlux.spec'  # Путь к .spec файлу, используемому PyInstaller для сборки приложения.
target_script = 'TwixFlux.py'  # Основной Python-скрипт, который будет упакован в исполняемый файл.
log_dir = 'pyinstaller'  # Директория, где могут храниться логи или файлы, связанные с процессом сборки.
spec_file_del = 'TwixFlux.spec'  # Имя файла .spec, который нужно удалить после сборки.
build_dir = 'build'  # Директория, в которой PyInstaller создает временные файлы во время сборки.
dist_dir = 'dist'  # Директория, где PyInstaller создает готовую сборку приложения.

def ensure_pyinstaller_installed():
    """
    Проверяет, установлен ли PyInstaller, и устанавливает его, если он отсутствует.
    Логирует процесс проверки и установки.
    """
    # Логируем начало проверки установки PyInstaller
    logger.info('🔍 Проверяем, установлен ли PyInstaller...')

    try:
        # Проверяем наличие PyInstaller с помощью команды 'pyinstaller --version'
        subprocess.run(
            ['pyinstaller', '--version'],
            check=True,  # Если команда завершится с ненулевым статусом, выбросится ошибка
            stdout=subprocess.PIPE,  # Перенаправляем стандартный вывод
            stderr=subprocess.PIPE,  # Перенаправляем стандартный вывод ошибок
            text=True  # Указываем, что вывод и ошибки должны быть в текстовом формате
        )
        # Если PyInstaller установлен, логируем успех
        logger.info('✅ PyInstaller уже установлен.')
    except (subprocess.CalledProcessError, FileNotFoundError):
        # В случае ошибки (PyInstaller не найден), логируем предупреждение
        logger.warning('❌ PyInstaller не установлен или установлен некорректно. Пытаемся установить...')
        try:
            # Пытаемся установить PyInstaller с помощью pip
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', 'pyinstaller'],
                check=True,  # Если команда завершится с ошибкой, выбрасывается исключение
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Если установка прошла успешно, логируем это
            logger.info('✅ PyInstaller успешно установлен.')
        except subprocess.CalledProcessError as e:
            # Если ошибка при установке, логируем ошибку и выводим логи
            logger.error('❌ Ошибка при установке PyInstaller.')
            logger.error(f'📜 Лог ошибки: {e.stderr}')
        except Exception as e:
            # Если произошла непредвиденная ошибка, логируем её
            logger.error(f'❌ Произошла непредвиденная ошибка при установке PyInstaller: {e}')

def remove_build_files():
    """Удаляет файлы и папки: TwixFlux.spec, build, dist и логирует процесс с эмодзи."""
    # Логируем начало процесса удаления
    logger.info('🧹 Начинаем удаление файлов и папок: TwixFlux.spec, build, dist')
    
    try:
        # Проверяем и удаляем файл .spec, если он существует
        if os.path.exists(spec_file_del):
            os.remove(spec_file_del)  # Удаляем файл
            logger.info(f'✅ Файл {spec_file_del} успешно удален.')
        else:
            # Логируем, что файл не найден и удаление не требуется
            logger.info(f'📝 Файл {spec_file_del} не найден. Удаление не требуется.')
        
        # Проверяем и удаляем папку build, если она существует
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)  # Удаляем папку
            logger.info(f'✅ Папка {build_dir} успешно удалена.')
        else:
            # Логируем, что папка не найдена и удаление не требуется
            logger.info(f'📝 Папка {build_dir} не найдена. Удаление не требуется.')
        
        # Проверяем и удаляем папку dist, если она существует
        if os.path.exists(dist_dir):
            shutil.rmtree(dist_dir)  # Удаляем папку
            logger.info(f'✅ Папка {dist_dir} успешно удалена.')
        else:
            # Логируем, что папка не найдена и удаление не требуется
            logger.info(f'📝 Папка {dist_dir} не найдена. Удаление не требуется.')
        
    except Exception as e:
        # Логируем ошибку, если возникла проблема при удалении
        logger.error(f'❌ Произошла ошибка при удалении файлов: {e}')

def start_first_build(target_script):
    """
    Выполняет первую сборку с параметрами --noconsole и логирует процесс с эмодзи.
    Ошибки при сборке не выводятся в лог, если они не критичны.

    :param target_script: Путь к целевому скрипту, который будет упакован с помощью PyInstaller.
    """
    # Логируем начало процесса сборки с параметром --noconsole
    logger.info('🧰 Начинаем первую сборку с параметром --noconsole')

    try:
        # Выполняем сборку с помощью PyInstaller, передавая необходимые параметры
        result = subprocess.run(
            ['pyinstaller', '--noconsole', target_script],  # Команда для PyInstaller
            check=True,  # Если команда завершится с ошибкой, возбуждается исключение
            stdout=subprocess.PIPE,  # Перехватываем стандартный вывод
            stderr=subprocess.PIPE,  # Перехватываем стандартный вывод ошибок
            text=True  # Получаем вывод в виде строк
        )

        # Если сборка успешна (returncode 0), логируем успешное завершение
        if result.returncode == 0:
            logger.info('✅ Первая сборка завершена успешно.')
        else:
            # Если возвращен код ошибки, логируем ошибку и сохраняем её в файл
            logger.error(f'❌ Ошибка при первой сборке с кодом {result.returncode}')
            if result.stderr:
                logger.error(f'❌ Ошибки при первой сборке: {result.stderr}')
                with open("build_errors.log", "w") as error_file:  # Сохраняем ошибки в файл
                    error_file.write(result.stderr)
                logger.info(f'📂 Ошибки сохранены в файл "build_errors.log".')

    except subprocess.CalledProcessError as e:
        # Логируем ошибку, если PyInstaller вызвал ошибку в процессе сборки
        logger.error(f'❌ Ошибка при первой сборке: {e}')
        exit(1)  # Завершаем программу с кодом 1 (ошибка)

    except Exception as e:
        # Логируем любые другие исключения, которые могут возникнуть
        logger.error(f'❌ Неизвестная ошибка при сборке: {e}')
        exit(1)  # Завершаем программу с кодом 1 (ошибка)

def replace_configuration_file():
    """
    Заменяет конфигурационный файл TwixFlux.spec.
    Логирует процесс с использованием эмодзи для визуализации статусов.
    """
    logger.info(f'🔄 Заменяем конфигурационный файл: {spec_file} → ./TwixFlux.spec')

    # Проверяем существование исходного файла
    if not os.path.exists(spec_file):
        logger.error(f'❌ Исходный файл {spec_file} не найден. Операция прервана.')
        return  # Выход из функции, если файл не найден, без остановки программы

    try:
        # Копируем файл
        shutil.copy(spec_file, 'TwixFlux.spec')
        logger.info('✅ Конфигурационный файл успешно заменен.')
    except PermissionError:
        # Ошибка прав доступа
        logger.error('❌ Ошибка прав доступа при замене конфигурационного файла. Проверьте разрешения.')
    except IOError as e:
        # Ошибка ввода/вывода
        logger.error(f'❌ Ошибка ввода/вывода: {e}')
    except Exception as e:
        # Логирование непредвиденной ошибки
        logger.error(f'❌ Произошла непредвиденная ошибка: {e}')
    finally:
        # Завершаем логирование процесса
        logger.info('📝 Завершение процесса замены конфигурационного файла.')

def start_second_build():
    """
    Выполняет вторую сборку проекта с использованием PyInstaller и флагами --clean и --noconfirm.
    Перед началом сборки удаляет папку dist/TwixFlux, если она существует.
    Логирует весь процесс с использованием эмодзи.
    """
    # Полный путь к папке dist/TwixFlux
    dist_path = os.path.join(os.getcwd(), 'dist', 'TwixFlux')
    
    # Удаление папки dist/TwixFlux, если она существует
    if os.path.exists(dist_path):
        logger.info('✅ Удаляем папку dist/TwixFlux перед началом второй сборки...')
        try:
            shutil.rmtree(dist_path)
            logger.info('✅ Папка dist/TwixFlux успешно удалена.')
        except Exception as e:
            # Ошибка при удалении папки
            logger.error(f'❌ Ошибка при удалении папки dist/TwixFlux: {e}')
            return  # Завершаем выполнение функции, так как удаление папки не удалось

    # Логируем начало сборки
    logger.info('🧰 Начинаем вторую сборку проекта с использованием флагов --clean и --noconfirm...')

    try:
        # Выполнение команды PyInstaller
        result = subprocess.run(
            ['pyinstaller', '--clean', '--noconfirm', 'TwixFlux.spec'],
            check=True,  # Выбрасывает исключение, если команда завершилась с ошибкой
            stdout=subprocess.PIPE,  # Захватываем стандартный вывод
            stderr=subprocess.PIPE,  # Захватываем вывод ошибок
            text=True  # Преобразуем вывод в строки
        )

        # Логируем успешное завершение сборки
        logger.info('✅ Вторая сборка завершена успешно.')
        if result.stdout:
            logger.info(f'📜 Лог сборки: {result.stdout}')

    except subprocess.CalledProcessError as e:
        # Логируем ошибки, если команда завершилась с ошибкой
        logger.error('❌ Ошибка во время выполнения второй сборки.')
        logger.error(f'💥 Код ошибки: {e.returncode}')
        logger.error(f'📜 Лог ошибок: {e.stderr}')

    except Exception as e:
        # Логируем непредвиденные ошибки
        logger.error(f'❌ Произошла непредвиденная ошибка: {e}')

def move_to_mac_os_and_go_back():
    # Логируем текущую рабочую директорию
    logger.info(f"🗺️ Текущая директория после перехода: {os.getcwd()}")

    # Определяем путь исходного файла и целевой директории
    src_file = "dist/TwixFlux"  # Путь к исходному файлу, который нужно переместить
    dest_dir = "dist/TwixFlux.app/Contents/MacOS/"  # Путь к целевой директории на MacOS

    # Проверка, существует ли исходный файл
    if not os.path.isfile(src_file):
        logger.error(f"❌ Ошибка: файл '{src_file}' не найден.")  # Логируем ошибку, если файл не найден
        return  # Выход из функции, если файл не найден

    # Проверка, существует ли целевая директория
    if not os.path.isdir(dest_dir):
        logger.error(f"❌ Ошибка: директория '{dest_dir}' не найдена.")  # Логируем ошибку, если директория не найдена
        return  # Выход из функции, если директория не найдена

    # Перемещение файла в целевую директорию
    try:
        shutil.move(src_file, os.path.join(dest_dir, os.path.basename(src_file)))  # Перемещаем файл
        logger.info(f"✅ Файл '{src_file}' успешно перемещен в '{dest_dir}'.")  # Логируем успех
    except Exception as e:
        logger.error(f"❌ Ошибка при перемещении файла: {e}")  # Логируем ошибку, если перемещение не удалось

def create_icns_from_png():
    # Определяем пути для файлов и директорий
    script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))  # Директория скрипта
    source_icon_path = 'icon.png'  # Путь к исходному файлу иконки
    iconset_dir = 'TwixFlux.iconset'  # Директория для хранения промежуточных иконок
    icns_file = 'TwixFlux.icns'  # Финальный файл .icns
    app_resource_dir = '../dist/TwixFlux.app/Contents/Resources'  # Директория для ресурсов приложения

    # Переход в директорию скрипта
    os.chdir(script_dir)

    # Шаг 1: Проверка наличия исходного файла иконки
    if not os.path.exists(source_icon_path):
        logger.error("❌ Исходный файл иконки не найден.")  # Логируем ошибку, если файл не найден
        exit(1)  # Завершаем выполнение, если файл отсутствует

    # Создание директории для иконок, если она не существует
    if not os.path.exists(iconset_dir):
        os.makedirs(iconset_dir)  # Создаем директорию для иконок
        logger.info(f"✅ Директория для иконок создана.")  # Логируем успешное создание

    # Массив размеров иконок для создания разных версий
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    for size in sizes:
        for scale in [1, 2]:  # Масштабирование иконок для разных плотностей пикселей
            new_size = size * scale  # Рассчитываем новый размер
            output_file = os.path.join(iconset_dir, f'icon_{new_size}x{new_size}.png')  # Путь для сохранения иконки

            # Масштабируем иконку с помощью утилиты sips
            subprocess.run(
                ['sips', '--resampleHeightWidth', str(new_size), str(new_size), source_icon_path, '--out', output_file],
                stdout=subprocess.DEVNULL,  # Отключаем вывод в консоль
                stderr=subprocess.DEVNULL   # Отключаем вывод ошибок
            )
            
            # Логируем информацию о размере иконки
            logger.info(f"🖼️ Иконка {new_size}x{new_size} сгенерирована.")

    # Шаг 2: Создание .icns файла из иконок
    subprocess.run(['iconutil', '--convert', 'icns', iconset_dir, '--output', icns_file])
    if os.path.exists(icns_file):
        logger.info(f"✅ Файл {icns_file} успешно создан.")  # Логируем успешное создание .icns файла
    else:
        logger.error(f"❌ Не удалось создать {icns_file}.")  # Логируем ошибку, если файл не создан
        exit(1)  # Завершаем выполнение, если не удалось создать файл

    # Шаг 3: Перемещение и переименование .icns файла в директорию ресурсов приложения
    if not os.path.exists(app_resource_dir):
        os.makedirs(app_resource_dir)  # Создаем директорию ресурсов, если она не существует
        logger.info(f"✅ Директория для ресурсов приложения создана.")  # Логируем создание

    # Путь для перемещения иконки
    target_path = os.path.join(app_resource_dir, 'icon-windowed.icns')
    shutil.move(icns_file, target_path)  # Перемещаем иконку в целевую директорию
    logger.info(f"🔄 Иконка перемещена и переименована.")  # Логируем успешное завершение операции

def run_signing_and_verification():
    # Список команд для подписания, проверки и удаления атрибутов
    commands = [
        ("Подписываем приложение", "sudo codesign --force --deep --sign - ~/Desktop/TwixFlux/dist/TwixFlux.app"),
        ("Проверяем подпись", "codesign --verify --deep --verbose ~/Desktop/TwixFlux/dist/TwixFlux.app"),
        ("Удаляем атрибут quarantine", "sudo xattr -r -d com.apple.quarantine ~/Desktop/TwixFlux/dist/TwixFlux.app")
    ]
    
    # Перебираем все команды и выполняем их
    for description, command in commands:
        try:
            # Выполнение команды с захватом вывода и ошибок
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Логируем успешное выполнение команды
            logger.info(f"✅ {description}: выполнено успешно.")
        except subprocess.CalledProcessError as e:
            # Логируем ошибку, если команда не выполнена
            logger.error(f"❌ Ошибка при выполнении команды '{command}':\n{e.stderr.decode()}")

if __name__ == '__main__':
    # Убеждаемся, что PyInstaller установлен в системе, иначе выполняем его установку
    # Эта функция проверяет, установлен ли PyInstaller. Если он не установлен, то будет выполнена его автоматическая установка.
    ensure_pyinstaller_installed()

    # Удаляем временные и промежуточные файлы сборки (папки build, dist и другие)
    # Это помогает избежать конфликтов и обеспечивает чистую сборку проекта
    # Функция удаляет все временные файлы, созданные во время предыдущих сборок, чтобы начать с чистого состояния.
    remove_build_files()

    # Запускаем первую сборку целевого скрипта (target_script)
    # Первая сборка генерирует необходимые файлы и структуру проекта
    # Это важный этап, на котором создается основная структура проекта и необходимые исходные файлы для дальнейшей работы.
    start_first_build(target_script)

    # Заменяем автоматически сгенерированный файл конфигурации TwixFlux.spec на пользовательский
    # Это позволяет настроить сборку проекта в соответствии с нашими требованиями
    # Пользовательский файл конфигурации помогает настроить сборку в соответствии с нуждами проекта (например, добавление дополнительных файлов или параметров).
    replace_configuration_file()

    # Выполняем вторую сборку проекта с флагами:
    # --clean: удаляет временные файлы предыдущих сборок
    # --noconfirm: отключает запросы на подтверждение во время сборки
    # Вторая сборка выполняет финальную упаковку проекта, очищая предыдущие файлы и автоматически подтверждая все запросы.
    start_second_build()

    # Перемещаем собранный файл в нужную директорию и возвращаемся назад
    # Эта функция перемещает финальный файл в требуемую директорию MacOS и затем возвращает текущую директорию в исходное состояние.
    move_to_mac_os_and_go_back()

    # Создаем и перемещаем иконку в нужное место
    # Эта функция создает иконку с именем "icon.png" и перемещает её в нужную директорию.
    create_icns_from_png()

    # Запускаем процесс подписания, проверки и удаления атрибута quarantine для приложения
    # Эта функция подписывает приложение, проверяет подпись и удаляет атрибут quarantine, если необходимо.
    run_signing_and_verification()