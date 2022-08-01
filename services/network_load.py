"""Расчет нагрузки сети."""
from datetime import datetime
from random import uniform


def interest_calculation() -> dict:
    """Генерация процента нагруженности сети."""
    if datetime.today().month == 1 or 6 <= datetime.today().month <= 8:
        if 0 <= datetime.today().weekday() <= 4:
            return {
                'average_load': round(15 + uniform(0, 5), 2),
                'maximum_load': round(15 + uniform(5, 7), 2)
            }
        else:
            return {
                'average_load': round(10 + uniform(0, 5), 2),
                'maximum_load': round(10 + uniform(5, 7), 2)
            }
    else:
        if 0 <= datetime.today().weekday() <= 4:
            return {
                'average_load': round(45 + uniform(5, 10), 2),
                'maximum_load': round(45 + uniform(10, 20), 2)
            }
        else:
            return {
                'average_load': round(42 + uniform(0, 5), 2),
                'maximum_load': round(42 + uniform(5, 10), 2)
            }
