import requests
from tools.logger import logger
from config import Config


class TelegramNotifier:
    """Класс для отправки уведомлений в Telegram"""

    def __init__(self, config=None):
        self.config = config or Config()
        self.bot_token = self.config.TELEGRAM_BOT_TOKEN
        self.chat_id = self.config.TELEGRAM_CHAT_ID

    def send_message(self, message):
        """
        Отправляет сообщение в Telegram

        Args:
            message (str): текст сообщения

        Returns:
            bool: успешность отправки
        """
        if not self.config.TELEGRAM_ENABLED:
            logger.debug("Telegram уведомления отключены в конфиге")
            return False

        if not self.bot_token or not self.chat_id:
            logger.warning("Telegram bot token или chat id не настроены")
            return False

        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }

            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()

            logger.debug("Уведомление отправлено в Telegram")
            return True

        except Exception as e:
            logger.error(f"Ошибка отправки уведомления в Telegram: {str(e)}")
            return False

    def send_critical_error(self, error_message):
        """Отправляет уведомление о критической ошибке"""
        message = f"{self.config.CRITICAL_ERROR_MESSAGE}\n\nОшибка: {error_message}"
        return self.send_message(message)

    def send_restart_success(self):
        """Отправляет уведомление об успешном перезапуске"""
        return self.send_message(self.config.RESTART_SUCCESS_MESSAGE)

    def send_startup(self):
        """Отправляет уведомление о запуске"""
        return self.send_message(self.config.STARTUP_MESSAGE)

    def send_shutdown(self):
        """Отправляет уведомление об остановке"""
        return self.send_message(self.config.SHUTDOWN_MESSAGE)