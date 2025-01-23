#!/bin/bash

# Переход на одну папку назад
cd ..

# Выводим текущую директорию после перехода
echo -e "🗺️ Текущая директория после перехода  \n📂 $(pwd)"

# Проверяем, что текущая директория это 'TwixFlux'
if [ "$(basename $(pwd))" == "TwixFlux" ]; then
    echo "✅ Мы находимся в папке 'TwixFlux'."
else
    echo "❌ Мы не находимся в папке 'TwixFlux'."
    exit
fi

# Функция для удаления папки myenv
remove_myenv() {
    echo "❌ Удаляем папку 'myenv'..."
    
    # Проверка существования папки myenv
    if [ -d "myenv" ]; then
        rm -rf myenv
        if [ $? -eq 0 ]; then
            echo "✅ Папка 'myenv' успешно удалена!"
        else
            echo "❌ Ошибка при удалении папки 'myenv'."
        fi
    else
        echo "🚨 Папка 'myenv' не существует."
    fi
}

# Проверяет, установлен ли Homebrew, и устанавливает его, если необходимо
check_brew() {
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew не установлен."
        echo "💡 Устанавливаю Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        if ! command -v brew &> /dev/null; then
            echo "❌ Не удалось установить Homebrew. Пожалуйста, установите его вручную."
            exit 1
        fi
        echo "✅ Homebrew успешно установлен."
    else
        echo "✅ Homebrew уже установлен."
    fi
}

# Проверяет, установлен ли Python 3 через Homebrew
check_python3() {
    if ! brew list python &> /dev/null; then
        echo "❌ Python 3 не найден. Устанавливаю через Homebrew..."
        brew install python
        if ! brew list python &> /dev/null; then
            echo "❌ Не удалось установить Python 3 через Homebrew."
            exit 1
        fi
        echo "✅ Python 3 успешно установлен через Homebrew."
    else
        echo "✅ Python 3 уже установлен."
    fi
}

# Создаёт виртуальное окружение
create_venv() {
    echo "🔧 Создаём виртуальное окружение..."
    
    python3 -m venv myenv
    
    if [ ! -d "myenv" ]; then
        echo "❌ Ошибка при создании виртуального окружения."
        exit 1
    fi
    
    echo "✅ Виртуальное окружение 'myenv' успешно создано."
}

# Активирует виртуальное окружение
activate_venv() {
    echo "🌟 Активируем виртуальное окружение..."
    
    if [ ! -d "myenv" ]; then
        echo "❌ Виртуальное окружение 'myenv' не найдено. Пожалуйста, создайте его с помощью create_venv."
        exit 1
    fi
    
    source myenv/bin/activate
    
    if ! command -v deactivate &> /dev/null; then
        echo "❌ Ошибка при активации виртуального окружения."
        exit 1
    fi

    echo "✅ Виртуальное окружение 'myenv' успешно активировано."
}

# Проверяет наличие файла requirements.txt и устанавливает зависимости
check_and_install_dependencies() {
    if [ ! -f "requirements.txt" ]; then
        echo "🚨 Файл 'requirements.txt' не найден. Пожалуйста, создайте его перед запуском скрипта."
        deactivate
        exit 1
    fi
    
    echo "✅ Файл 'requirements.txt' найден."
    
    echo "📦 Устанавливаем зависимости из 'requirements.txt'..."
    
    # Полное подавление вывода
    pip install -r requirements.txt --quiet > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✅ Установка зависимостей завершена успешно!"
    else
        echo "❌ Ошибка при установке зависимостей."
        echo "👉 Попробуйте запустить установку зависимостей снова."
        deactivate
        exit 1
    fi
}

install_editable_mode() {
    # Проверяем, установлен ли setuptools
    if ! pip show setuptools > /dev/null 2>&1; then
        echo "❌ 'setuptools' не найден. Устанавливаем..."
        pip install setuptools
        if [ $? -eq 0 ]; then
            echo "✅ 'setuptools' успешно установлен!"
        else
            echo "❌ Ошибка при установке 'setuptools'."
            return 1
        fi
    else
        echo "✅ 'setuptools' уже установлен."
    fi

    # Если файл setup.py существует, удаляем его
    if [ -f "setup.py" ]; then
        echo "✅ Файл 'setup.py' найден. Удаляем..."
        rm setup.py
        echo "✅ Файл 'setup.py' успешно удален."
    fi

    # Создаем новый файл setup.py
    echo "from setuptools import setup, find_packages

setup(
    name='TwixFlux',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)" > setup.py

    # Проверяем успешность создания файла setup.py
    if [ -f "setup.py" ]; then
        echo "✅ Файл 'setup.py' успешно создан!"
    else
        echo "❌ Ошибка при создании файла 'setup.py'."
        return 1
    fi

    # Выполняем команду pip install -e .
    if pip install -e . > /dev/null 2>&1; then
        echo "✅ Установка в режиме редактирования прошла успешно!"
    else
        echo "❌ Ошибка при установке."
    fi
}

# Основной процесс настройки
setup_environment() {
    remove_myenv
    check_brew
    check_python3
    create_venv
    activate_venv
    check_and_install_dependencies
    install_editable_mode
}

# Финальное сообщение о завершении настройки
finalize_setup() {
    echo "🎉 Настройка завершена!"
}

# Запуск процесса установки
setup_environment

# Завершаем настройку
finalize_setup