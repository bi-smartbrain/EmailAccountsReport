from datetime import datetime as dt


def compare_dates(date1, date2):
    """
    Возвращает более позднюю из двух дат
    """
    # Преобразуем строки в объекты datetime
    dt1 = dt.fromisoformat(date1)
    dt2 = dt.fromisoformat(date2)

    if dt1 >= dt2:
        return date1
    elif dt2 > dt1:
        return date2

