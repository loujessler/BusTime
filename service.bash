#!/bin/bash

# Путь до виртуального окружения Python
VENV_PATH="/BusTimes/env"

# Путь до файла с Python скриптом
PYTHON_SCRIPT_PATH="/BusTimes/bot.py"

# Путь до файла с зависимостями
REQUIREMENTS_PATH="/BusTimes/requirements.txt"

# Функция для запуска Python скрипта
start() {
  # Активация виртуального окружения
  source $VENV_PATH/bin/activate

  # Проверка и установка пакетных зависимостей
  pip install -r $REQUIREMENTS_PATH

  # Запуск Python скрипта
  nohup python3 $PYTHON_SCRIPT_PATH > bot.log 2>&1 &
  echo $! > save_pid.txt
}

# Функция для остановки Python скрипта
stop() {
  kill $(cat save_pid.txt)
  rm save_pid.txt
}

# Парсинг аргументов командной строки
case $1 in
  start|restart)
    start
    ;;
  stop)
    stop
    ;;
  *)
    echo "Usage: $0 {start|stop|restart}"
    exit 1
esac

exit 0
