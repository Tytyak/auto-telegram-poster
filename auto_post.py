import os
import requests
import qrcode
from datetime import datetime

# забираем из окружения
TOKEN   = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
LONG_URL= os.getenv("LONG_URL")

def shorten_with_isgd(long_url: str) -> str:
    """Сокращает через is.gd и возвращает короткую ссылку."""
    resp = requests.get(
        "https://is.gd/create.php",
        params={"format": "simple", "url": long_url},
    )
    resp.raise_for_status()
    return resp.text.strip()

def make_qr(link: str, filename: str = "short_qr.png"):
    """Генерирует PNG-файл с QR-кодом."""
    img = qrcode.make(link)
    img.save(filename)
    return filename

def post_to_telegram(image_path: str, caption: str):
    """Отправляет фото в канал."""
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    with open(image_path, "rb") as f:
        files = {"photo": f}
        data = {"chat_id": CHAT_ID, "caption": caption}
        r = requests.post(url, files=files, data=data)
        r.raise_for_status()

def main():
    # 1) Сокращаем ссылку
    short = shorten_with_isgd(LONG_URL)

    # 2) Генерируем QR-код
    img_file = make_qr(short)

    # 3) Формируем подпись
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    caption = f"Ваше предложение: {short}\n\nGenerated at {now}"

    # 4) Шлём в Telegram
    post_to_telegram(img_file, caption)

    print(f"Posted successfully at {now}")

if __name__ == "__main__":
    main()
