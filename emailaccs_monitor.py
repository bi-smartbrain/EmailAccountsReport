import time
from datetime import datetime

from tools.close import get_email_accounts, get_users
from tools.sheets import write_spread_sheet
from tools.logger import logger
from report_generator import generate_email_accounts_report
from config import Config
from tools.telegram_notifier import TelegramNotifier


class EmailAccountsMonitor:
    """Монитор состояния email-аккаунтов в CRM Close"""

    def __init__(self, config=None):
        self.config = config or Config()
        self.notifier = TelegramNotifier(self.config)
        self.running = True
        self.retry_count = 0

    def run(self):
        """Основной цикл выполнения мониторинга"""
        # Уведомление о запуске
        self.notifier.send_startup()
        logger.info("Запуск мониторинга email-аккаунтов...")

        while self.running:
            try:
                self._run_iteration()
                self.retry_count = 0  # Сброс счетчика ошибок при успешной итерации
                self._wait_next_iteration()

            except KeyboardInterrupt:
                logger.info("Получен сигнал прерывания. Завершение работы...")
                self.notifier.send_shutdown()
                self.running = False

            except Exception as e:
                self.retry_count += 1
                logger.error(f"Ошибка в основном цикле (попытка {self.retry_count}): {str(e)}")
                self._handle_error(e)

    def _run_iteration(self):
        """Выполняет одну итерацию сбора данных и генерации отчета"""
        logger.info("Начало сбора данных...")

        # Получение данных
        accounts = get_email_accounts()
        users = get_users()

        logger.info(f"Получено {len(accounts)} аккаунтов и {len(users)} пользователей")

        # Генерация отчета
        report = generate_email_accounts_report(accounts, users)

        # Запись в Google Sheets
        write_spread_sheet(
            self.config.SPREAD_NAME,
            self.config.OUT_SHEET_NAME,
            report
        )

        logger.info(f"Отчет успешно обновлен: {datetime.now()}")

    def _wait_next_iteration(self):
        """Ожидание перед следующей итерацией"""
        logger.debug(f"Ожидание {self.config.UPDATE_INTERVAL} секунд до следующего обновления...")
        time.sleep(self.config.UPDATE_INTERVAL)

    def _handle_error(self, error):
        """Обработка ошибок в соответствии с конфигурацией"""
        # Отправка уведомления о критической ошибке
        self.notifier.send_critical_error(str(error))

        if self.config.RESTART_ON_CRITICAL_ERROR:
            logger.info(f"Перезапуск через {self.config.ERROR_RETRY_DELAY} секунд...")
            time.sleep(self.config.ERROR_RETRY_DELAY)

            # Уведомление об успешном перезапуске
            self.notifier.send_restart_success()
            logger.info("Скрипт успешно перезапущен после ошибки")
        else:
            self.running = False
            self.notifier.send_shutdown()

    def stop(self):
        """Остановка мониторинга"""
        self.running = False
        self.notifier.send_shutdown()
        logger.info("Мониторинг остановлен")