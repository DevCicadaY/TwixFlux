#!/bin/bash

# Функция для удаления директории .TwixFlux
remove_twixflux_directory() {
  local USER_HOME="$HOME"  # Определяем домашнюю директорию пользователя
  local TWIXFLUX_DIR="$USER_HOME/.TwixFlux"  # Определяем путь к директории .TwixFlux

  # Проверяем, существует ли директория .TwixFlux
  if [ -d "$TWIXFLUX_DIR" ]; then
    # Если директория существует, удаляем её
    rm -rf "$TWIXFLUX_DIR"
    echo "✅ Директория .TwixFlux успешно удалена."
  else
    # Если директория не существует
    echo "🚨 Директория .TwixFlux не найдена."
  fi
}

# Функция для удаления пароля из ключницы
remove_files_and_folders() { 
    local service_name="TwixFlux"  # Имя сервиса задаём внутри функции
    # Проверка на наличие пароля в ключнице перед удалением
    if security find-generic-password -s "$service_name" &>/dev/null; then
        echo "🔑 ✅ Пароль для $service_name найден, удаляю..."
        security delete-generic-password -s "$service_name" &>/dev/null
        echo "✅ Пароль для $service_name удалён."
    else
        echo "🚨 Пароль для $service_name не найден."
    fi
}

# Функция для удаления файлов с префиксом _MEI
cleanup_meim_files() {
    # Путь к папке
    local dir="/private/var/folders/1j/8q51xcjs5g7g1nx9wd8tws3r0000gn/T"
    
    # Ищем файлы с префиксом "_MEI"
    local files=$(ls "$dir" | grep "_MEI")
    
    # Проверяем, есть ли такие файлы
    if [ -n "$files" ]; then
        echo "🗑️ Файлы с префиксом _MEI найдены:"
        echo "$files"
        
        # Удаляем найденные файлы
        for file in $files; do
            rm -rf "$dir/$file"
            echo "✅ Удалён файл: $file"
        done
    else
        echo "🚨 Файлы с префиксом _MEI не найдены."
    fi
}

# Вызов функций
remove_twixflux_directory  # Удаляет директорию .TwixFlux
cleanup_meim_files         # Очищает файлы с префиксом _MEI
remove_files_and_folders   # Удаляет пароли и связанные файлы