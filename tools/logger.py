from loguru import logger
from config import Config


# Настройка файлового логгера
if Config.LOG_TO_FILE:
    logger.add(
        Config.LOG_FILE,
        level=Config.LOG_LEVEL,
        rotation="1 day",  # Ротация каждый день
        retention="7 days",  # Хранить 7 дней
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )

def setup_logger():
    """Настройка логгера"""
    return logger
