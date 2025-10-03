from closeio_api import Client
import tools.color_prints as p
from tools.env_loader import SECRETS_PATH
import os

api_key = os.getenv('CLOSE_API_KEY_MARY')
api = Client(api_key)


def get_email_accounts():
    """получает все емаил-аккаунты из Клоуз"""

    params = {
        "_skip": 0,
        "_limit": 100
    }

    accs = []
    p.print_info("Запрашиваем email-аккаунты")
    while True:
        resp = api.get('connected_account', params=params)
        accs.extend(resp['data'])
        if resp['has_more']:
            params['_skip'] += params['_limit']
            p.print_info(f'{len(accs)} получено')
        else:
            p.print_info(f'Всего {len(accs)} email-аккаунтов получено')
            return accs


def get_users():
    params = {}
    resp = api.get('user', params=params)
    return resp['data']


def get_user_names():
    """
    формирует словарь с полными именами Клоу-юзеров по форме {'user_id':'user_name'}
    """
    users = get_users()
    user_names = {}
    for user in users:
        user_id = user['id']
        first_name = user.get('first_name', '')
        last_name = user.get('last_name', '')
        user_name = first_name
        if last_name:
            user_name += f" {last_name}"
        user_names[user_id] = user_name
    return user_names

