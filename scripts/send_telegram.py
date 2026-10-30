"""Verilen metin dosyasını Telegram'a gönderir.

Kullanım: python scripts/send_telegram.py mesajlar/2026-10-30.md
Ortam değişkenleri: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
"""
import json
import os
import sys
import urllib.error
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
    try:
        with urllib.request.urlopen(istek, timeout=30) as yanit:
            sonuc = json.load(yanit)
    except urllib.error.HTTPError as e:
        hata(f"Telegram HTTP {e.code}: {e.read().decode(errors='replace')}")
    if not sonuc.get("ok"):
        hata(f"Telegram hatası: {sonuc}")


def hata(mesaj: str) -> None:
    """Hatayı hem loga hem de Actions özet sayfasına yazar."""
    print(mesaj)
    ozet = os.environ.get("GITHUB_STEP_SUMMARY")
    if ozet:
        with open(ozet, "a", encoding="utf-8") as f:
            f.write(f"### ❌ Gönderim hatası\n\n```\n{mesaj}\n```\n")
    print(f"::error::{mesaj}")
    raise SystemExit(1)


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token:
        hata("TELEGRAM_BOT_TOKEN secret'ı boş ya da bulunamadı.")
    if not chat_id:
        hata("TELEGRAM_CHAT_ID secret'ı boş ya da bulunamadı.")
    if ":" not in token:
        hata("TELEGRAM_BOT_TOKEN biçimi hatalı (içinde ':' olmalı).")
    with open(sys.argv[1], encoding="utf-8") as f:
        metin = f.read()
    for parca in parcala(metin):
        gonder(token, chat_id, parca)
    print(f"Gönderildi: {sys.argv[1]}")


if __name__ == "__main__":
    main()
