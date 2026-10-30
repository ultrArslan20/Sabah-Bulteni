# Sabah Bülteni

Her sabah Claude tarafından hazırlanan bülten `mesajlar/` klasörüne yazılır;
GitHub Actions bu dosyayı otomatik olarak Telegram'a gönderir.

## Gerekli GitHub Secrets
- `TELEGRAM_BOT_TOKEN` — BotFather'dan alınan token
- `TELEGRAM_CHAT_ID` — mesajın gideceği sohbetin kimliği

## Elle test
Actions → "Telegram'a gönder" → Run workflow
