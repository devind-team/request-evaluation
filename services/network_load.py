"""Расчет нагрузки сети."""
from datetime import datetime
from random import uniform


def interest_calculation() -> dict:
    """Генерация процента нагруженности сети."""
    week_day = datetime.today().weekday()
    if 0 <= week_day <= 4:
        return {
            'average_load': round(45 + uniform(5, 10), 2),
            'maximum_load': round(45 + uniform(10, 20), 2)
        }
    else:
        return {
            'average_load': round(42 + uniform(0, 5), 2),
            'maximum_load': round(42 + uniform(5, 10), 2)
        }
