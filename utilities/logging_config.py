import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
import glob
import time
from pathlib import Path

# Директория для логов

project_root = Path(__file__).resolve().parent.parent
LOG_DIR = str(project_root / 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Формат имени файла лога: run_dd.mm.yy.log
LOG_FILE = os.path.join(LOG_DIR, f"run_{datetime.now().strftime('%d.%m.%y')}.log")

# Настройка логгера
logger = logging.getLogger("TestLogger")
logger.setLevel(logging.INFO)

# Формат сообщений лога
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Обработчик для записи в файл с ротацией по дням
file_handler = TimedRotatingFileHandler(LOG_FILE, when="midnight", interval=1, backupCount=30, encoding='utf-8')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

# Обработчик для вывода в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Добавление обработчиков к логгеру
logger.addHandler(file_handler)

# Функция для удаления логов старше 30 дней
def clean_old_logs():
    now = time.time()
    thirty_days_ago = now - 30 * 24 * 60 * 60
    log_files = glob.glob(os.path.join(LOG_DIR, "run_*.log"))
    
    for log_file in log_files:
        if os.path.getmtime(log_file) < thirty_days_ago:
            try:
                os.remove(log_file)
                logger.info(f"Deleted old log file: {log_file}")
            except Exception as e:
                logger.error(f"Failed to delete log file {log_file}: {e}")

clean_old_logs()