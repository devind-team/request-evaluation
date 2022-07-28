"""Расчет нагрузки сети."""
from datetime import datetime
from random import uniform


def interest_calculation() -> dict:
    """Генерация процента нагруженности сети."""

    week_day = datetime.today().weekday()
    if 0 <= week_day <= 4:
        return {
            'average_load': 45 + uniform(5, 10),
            'maximum_load': 45 + uniform(10, 20)
        }
    else:
        return {
            'average_load': 42 + uniform(0, 5),
            'maximum_load': 42 + uniform(5, 10)
        }
