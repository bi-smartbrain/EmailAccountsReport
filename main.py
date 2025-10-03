import time
from tools.logger import logger
from emailaccs_monitor import EmailAccountsMonitor
from config import Config
from tools.telegram_notifier import TelegramNotifier


def main():
    """Основная функция запуска мониторинга"""
    config = Config()
    notifier = TelegramNotifier(config)
    monitor = EmailAccountsMonitor(config)

    try:
        monitor.run()
    except Exception as e:
        logger.critical(f"Критическая ошибка в мониторинге: {str(e)}")

        # Отправка уведомления о критической ошибке
        notifier.send_critical_error(str(e))

        if config.RESTART_ON_CRITICAL_ERROR:
            logger.info(f"Перезапуск через {config.ERROR_RETRY_DELAY} секунд...")
            time.sleep(config.ERROR_RETRY_DELAY)

            # Уведомление об успешном перезапуске
            notifier.send_restart_success()
            logger.info("Перезапуск мониторинга...")
            main()  # Рекурсивный перезапуск
        else:
            notifier.send_shutdown()


if __name__ == "__main__":
    main()