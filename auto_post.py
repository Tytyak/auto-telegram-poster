"""
Auto Post Every 2h — исправленный скрипт без упоминания micropip

Этот скрипт автоматически сокращает вашу ссылку, генерирует QR-код и публикует его в Telegram-канале каждые 2 часа.

1) Параметры (TOKEN, CHAT_ID, LONG_URL) берутся из переменных окружения или задаются в коде.
2) Запуск: `python3 auto_post.py`, требуется установить пакеты requests и qrcode.
"""

import sys
# ---------------------------------------------
# Проверяем наличие необходимых библиотек
# ---------------------------------------------
try:
    import time
    import requests
    import qrcode
    import os
except ModuleNotFoundError as e:
    print(f"Ошибка: не найден модуль '{e.name}'. Установите его командой: pip install {e.name}")
    sys.exit(1)

# =============================================
# 1) Сокращение ссылок через is.gd (не менять)
# =============================================

def shorten_with_isgd(long_url):
    resp = requests.get(
        "https://is.gd/create.php",
        params={"format": "simple", "url": long_url}
    )
    resp.raise_for_status()
    return resp.text.strip()

# =============================================
# 2) Генерация QR-кода (не менять)
# =============================================

def make_qr(link, filename="short_qr.png"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    return filename

# =============================================
# 3) Конфигурация (заменить своими данными)
# =============================================
# 3.1. Ваш токен от BotFather или переменная окружения TELEGRAM_TOKEN
TOKEN = os.getenv("TELEGRAM_TOKEN", "7994937367:AAEqTc4l9ltk0Sg4Rx0K4ytme5Xl5P1KrZk")
# 3.2. Юзернейм вашего канала (с @) или переменная окружения CHAT_ID
CHAT_ID = os.getenv("CHAT_ID", "@DeystvuyBot1")
# 3.3. Ваша целевая ссылка или переменная окружения LONG_URL
LONG_URL = os.getenv("LONG_URL", "https://otieu.com/4/9562866")

# =============================================
# 4) Отправка фото в Telegram (не менять)
# =============================================

def post_to_telegram(text, image_path):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    with open(image_path, "rb") as img_file:
        files = {"photo": img_file}
        data = {"chat_id": CHAT_ID, "caption": text}
        resp = requests.post(url, files=files, data=data)
    resp.raise_for_status()

# =============================================
# 5) Основной цикл каждые 2 часа (не менять)
# =============================================

if __name__ == "__main__":
    while True:
        try:
            short_link = shorten_with_isgd(LONG_URL)
            qr_file = make_qr(short_link)
            caption = f"Ваша ссылка: {short_link}"
            post_to_telegram(caption, qr_file)
            print(f"Posted successfully at {time.asctime()}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        time.sleep(7200)
