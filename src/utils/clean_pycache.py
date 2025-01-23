import os  # Импортируем модуль для работы с операционной системой
import shutil  # Импортируем модуль для работы с файловой системой, включая удаление директорий

def remove_pycache_in_project():
    """
    Определяет корневую директорию проекта и удаляет все каталоги __pycache__.
    """
    from src.utils.logger import logger  # Локальный импорт логгера для использования в данной функции

    # Определяем корень проекта относительно текущего пути
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))  # Путь к корню проекта
    logger.info(f"🔍 Поиск и удаление __pycache__ в проекте: {project_root}")  # Логируем начало процесса поиска __pycache__

    # Проходим по всем директориям и файлам проекта
    for root, dirs, files in os.walk(project_root):  # os.walk позволяет рекурсивно обходить все каталоги и файлы
        for dir_name in dirs:  # Для каждой директории
            if dir_name == "__pycache__":  # Проверяем, если это директория __pycache__
                pycache_path = os.path.join(root, dir_name)  # Формируем путь к __pycache__
                try:
                    shutil.rmtree(pycache_path)  # Удаляем всю директорию __pycache__
                    logger.info(f"✅ Удалён: {pycache_path}")  # Логируем успешное удаление
                except Exception as e:  # Обрабатываем возможные ошибки при удалении
                    logger.error(f"❌ Ошибка при удалении {pycache_path}: {e}")  # Логируем ошибку, если удаление не удалось