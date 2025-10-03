import gspread
from gspread.utils import rowcol_to_a1
from tools.env_loader import SECRETS_PATH
import os

SERVICE_ACCOUNT_FILE = os.path.join(SECRETS_PATH, 'service_account.json')
gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)


def write_spread_sheet(spread, sheet, report):
    """
    Очищает лист гугл таблицы и записывает на него отчет
    :param spread: гугл таблица (название)
    :param sheet: название листа
    :param report: отчет в виде списка списков
    :return: None
    """
    sh = gc.open(spread)
    worksheet = sh.worksheet(sheet)
    worksheet.clear()
    print(f"Лист {sheet} в таблице {spread} очищен")

    # Получить размеры отчета (количество строк и столбцов)
    num_rows = len(report)
    num_cols = len(report[0])

    # Получить диапазон для записи данных
    start_cell = rowcol_to_a1(1, 1)
    end_cell = rowcol_to_a1(num_rows, num_cols)

    # Записать значения в диапазон
    cell_range = f"{start_cell}:{end_cell}"
    worksheet.update(report, cell_range, value_input_option="user_entered")

    print("Отчет записан")