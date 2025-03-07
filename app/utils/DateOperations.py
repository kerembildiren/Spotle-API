from datetime import datetime

from app import config


def is_new_day():
    today = datetime.now().date()

    if today != config.LAST_DATE:
        config.LAST_DATE = today  # Yeni günü güncelle
        return True  # Yeni gün başladı

    return False  # Aynı gün içindeyiz