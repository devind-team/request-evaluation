"""Расчет нагрузки сети."""
from datetime import datetime
from random import uniform


def interest_calculation() -> dict:
    """Генерация процента нагруженности сети."""
    if datetime.today().month == 1 or 6 <= datetime.today().month <= 8:
        return week_day(average_load=42, maximum_load=45, start=5, average=10, end=20)
    else:
        return week_day(average_load=15, maximum_load=42, start=0, average=5, end=10)


def week_day(average_load: int, maximum_load: int, start: int, average: int, end: int) -> dict:
    """Вычисление нагрузки в зависимости от дня недели."""
    if 0 <= datetime.today().weekday() <= 4:
        return {
            'average_load': round(average_load + uniform(start, average), 2),
            'maximum_load': round(maximum_load + uniform(average, end), 2)
        }
    else:
        return {
            'average_load': round(3 + uniform(0, 3), 2),
            'maximum_load': round(9 + uniform(0, 2), 2)
        }
