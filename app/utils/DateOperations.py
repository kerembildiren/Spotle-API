import time
from datetime import datetime

from app import config


def is_new_day():
    today = datetime.now().date()

    if today != config.LAST_DATE:
        config.LAST_DATE = today  # Yeni günü güncelle
        return True  # Yeni gün başladı

    return False  # Aynı gün içindeyiz

def has_one_day_passed(timestamp):
    # Mevcut zaman (şu an) Unix zaman damgası formatında (saniye cinsinden)
    current_time = time.time()

    # 1 gün = 86400 saniye
    one_day_in_seconds = 86400

    # Eğer belirtilen timestamp üzerinden 1 gün geçmişse True döner
    return (current_time - timestamp) >= one_day_in_seconds