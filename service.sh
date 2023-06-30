#!/bin/bash

# Путь до виртуального окружения Python
VENV_PATH="./env"

# Путь до файла с Python скриптом
PYTHON_SCRIPT_PATH="./run.py"

# Путь до файла с зависимостями
REQUIREMENTS_PATH="./requirements.txt"

# Функция для запуска Python скрипта
start() {
  # Проверка, запущен ли уже скрипт
  if [ -e save_pid.txt ]; then
    if ps -p $(cat save_pid.txt) > /dev/null; then
      echo "The script is already running. Stop it first."
      exit 1
    fi
  fi

  # Активация виртуального окружения
  source $VENV_PATH/bin/activate

  # Проверка, запущен ли скрипт внутри виртуального окружения
  if [ -z "$VIRTUAL_ENV" ]; then
    echo "The script is not running inside a virtual environment. Please start the script inside a virtual environment."
    exit 1
  fi

  # Проверка и установка пакетных зависимостей
  pip install -r $REQUIREMENTS_PATH

  # Запуск Python скрипта
  nohup python3 $PYTHON_SCRIPT_PATH > bot.log 2>&1 &
  echo $! > save_pid.txt
}

# Функция для остановки Python скрипта
stop() {
  if [ ! -e save_pid.txt ]; then
    echo "The script is not running."
    exit 1
  else
    kill $(cat save_pid.txt)
    rm save_pid.txt
  fi
}

# Парсинг аргументов командной строки
case $1 in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart)
    stop
    start
    ;;
  *)
    echo "Usage: $0 {start|stop|restart}"
    exit 1
esac

exit 0
