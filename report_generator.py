from datetime import datetime
from tools.utilities import compare_dates
from config import Config


def generate_email_accounts_report(accounts, users):
    """
    Генерирует отчет о состоянии email-аккаунтов

    Args:
        accounts: список email-аккаунтов
        users: список пользователей

    Returns:
        list: матрица данных для отчета
    """
    config = Config()

    report = [config.REPORT_COLUMNS]

    # Создание словаря пользователей для быстрого поиска
    users_dict = {user['id']: f"{user['first_name']} {user['last_name']}"
                  for user in users}

    # Обработка каждого аккаунта
    for account in accounts:
        row = _process_account(account, users_dict)
        report.append(row)

    return report


def _process_account(account, users_dict):
    """
    Обрабатывает данные одного аккаунта и возвращает строку для отчета

    Args:
        account: данные аккаунта
        users_dict: словарь пользователей {id: имя}

    Returns:
        list: строка данных для отчета
    """
    # Базовые данные аккаунта
    user_name = users_dict.get(account['user_id'], 'Unknown User')
    date_created = account['date_created'].split("T")[0]

    # Данные SMTP и IMAP
    smtp_data = account.get('smtp', {})
    imap_data = account.get('imap', {})

    # Дата обновления
    date_updated = _get_updated_date(imap_data, smtp_data)

    # Последнее использование
    last_used_data = _get_last_used_info(account)

    # Формирование строки отчета
    row = [
        user_name,
        date_created,
        account['email'],
        account['send_status'],
        account['receive_status'],
        date_updated,
        len(account['identities']),
        account['default_identity']['name'],
        account['default_identity']['email'],
        " | ".join(account['enabled_features']),
        date_created[:7],  # month_created
        date_updated[:7] if date_updated else '',  # month_updated
        str(datetime.now()),  # report_updated
        account['_type'].split("_")[0],
        account['default_identity']['email'].split("@")[1],
        last_used_data['date'],
        last_used_data['month'],
        account.get('latest_receive_error', 'None') or 'None',
        account.get('latest_send_error', 'None') or 'None',
        account['id']
    ]

    return row


def _get_updated_date(imap_data, smtp_data):
    """
    Определяет дату обновления на основе IMAP и SMTP данных

    Args:
        imap_data: данные IMAP
        smtp_data: данные SMTP

    Returns:
        str: дата обновления
    """
    smtp_date = smtp_data.get('date_updated', '') if smtp_data else ''
    imap_date = imap_data.get('date_updated', '') if imap_data else smtp_date

    if smtp_date:
        return compare_dates(imap_date, smtp_date).split(" ")[0]
    return imap_date


def _get_last_used_info(account):
    """
    Извлекает информацию о последнем использовании аккаунта

    Args:
        account: данные аккаунта

    Returns:
        dict: информация о последнем использовании
    """
    last_used_date = "no_used"
    if account.get('lead_suggestions_updated_at'):
        last_used_date = account['lead_suggestions_updated_at'].split("T")[0]

    last_used_month = last_used_date[:7] if last_used_date != "no_used" else "no_used"

    return {
        'date': last_used_date,
        'month': last_used_month
    }