"""Verilen metin dosyasını Telegram'a gönderir.

Kullanım: python scripts/send_telegram.py mesajlar/2026-10-30.md
Ortam değişkenleri: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
"""
import json
import os
import sys
import urllib.request

LIMIT = 4000  # Telegram sınırı 4096 karakter; pay bırakıyoruz


def parcala(metin: str) -> list[str]:
    parcalar, mevcut = [], ""
    for satir in metin.splitlines(keepends=True):
        if len(mevcut) + len(satir) > LIMIT and mevcut:
            parcalar.append(mevcut)
            mevcut = ""
        while len(satir) > LIMIT:
            parcalar.append(satir[:LIMIT])
            satir = satir[LIMIT:]
        mevcut += satir
    if mevcut.strip():
        parcalar.append(mevcut)
    return parcalar


def gonder(token: str, chat_id: str, metin: str) -> None:
    veri = json.dumps({
        "chat_id": chat_id,
        "text": metin,
        "disable_web_page_preview": True,
    }).encode()
    istek = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=veri,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(istek, timeout=30) as yanit:
        sonuc = json.load(yanit)
    if not sonuc.get("ok"):
        raise SystemExit(f"Telegram hatası: {sonuc}")


def main() -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    with open(sys.argv[1], encoding="utf-8") as f:
        metin = f.read()
    for parca in parcala(metin):
        gonder(token, chat_id, parca)
    print(f"Gönderildi: {sys.argv[1]}")


if __name__ == "__main__":
    main()
