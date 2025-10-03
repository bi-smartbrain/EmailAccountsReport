import os
from datetime import time
from tools.env_loader import setup_environment

# Инициализация переменных окружения
setup_environment()


class Config:
    # Основные настройки
    SPREAD_NAME = "Close Email Accounts v2.0"
    OUT_SHEET_NAME = "emailaccts_api_report"

    # Настройки цикла обновления
    UPDATE_INTERVAL = 300  # секунд (5 минут)

    # Настройки API
    API_TIMEOUT = 30  # секунд
    MAX_RETRIES = 3
    RETRY_DELAY = 60  # секунд

    # Логика ошибок
    RESTART_ON_CRITICAL_ERROR = True  # Перезапуск при критической ошибке
    ERROR_RETRY_DELAY = 300  # секунд (5 минут) перед перезапуском при ошибке

    # Логирование
    LOG_TO_FILE = True
    LOG_FILE = "logs.log"
    LOG_LEVEL = "INFO"

    # Настройки отчета
    REPORT_COLUMNS = [
        'user', 'date_created', 'email', 'send_status', 'receive_status',
        'date_updated', 'qty_identities', 'avatar_name', 'avatar_email',
        'enabled_features', 'month_created', 'month_updated', 'report_updated',
        'type', 'domain', 'last_used_date', 'last_used_month',
        'latest_receive_error', 'latest_send_error', 'emailacc_id'
    ]

    # Настройки Telegram уведомлений
    TELEGRAM_ENABLED = True
    TELEGRAM_BOT_TOKEN = os.getenv('TG_TOKEN', '')
    TELEGRAM_CHAT_ID = os.getenv('CHAT_ID_1', '')

    # Текст уведомлений
    script_name = "EmailAccountsReport.py"
    CRITICAL_ERROR_MESSAGE = f"❌ {script_name} КРИТИЧЕСКАЯ ОШИБКА"
    RESTART_SUCCESS_MESSAGE = f"✅ {script_name} успешно перезапущен"
    STARTUP_MESSAGE = f"🟢 {script_name} запущен"
    SHUTDOWN_MESSAGE = f"⏹️ {script_name} остановлен"

    # Валидация конфигурации
    def __init__(self):
        self._validate_config()

    def _validate_config(self):
        """Проверяет корректность конфигурации"""
        if self.TELEGRAM_ENABLED:
            if not self.TELEGRAM_BOT_TOKEN:
                raise ValueError("TELEGRAM_BOT_TOKEN не найден в переменных окружения")
            if not self.TELEGRAM_CHAT_ID:
                raise ValueError("TELEGRAM_CHAT_ID не найден в переменных окружения")