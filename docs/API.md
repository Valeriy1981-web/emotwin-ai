# EmoTwin AI API Документация

## Общая информация

### Базовый URL
`https://api.emotwin.ru/v1`

### Версии API
* Текущая версия: **v1**
* Дата релиза: 2024-05-15

---

## Аутентификация

### Получение токена
Для работы с API требуется токен авторизации.

**POST /auth/token**
```json
{
  "username": "string",
  "password": "string"
}
# EmoTwin AI API Документация

## Общая информация

### Базовый URL
`https://api.emotwin.ru/v1`

### Версии API
* Текущая версия: **v1**
* Дата релиза: 2024-05-15

---

## Аутентификация

### Получение токена
Для работы с API требуется токен авторизации.

**POST /auth/token**
```json
{
  "username": "string",
  "password": "string"
}
{
  "status": "ok",
  "message": "EmoTwin AI API работает!",
  "timestamp": "2024-05-15T12:30:45Z"
}
{
  "text": "string"
}
{
  "text": "Исходный текст",
  "emotions": {
    "joy": 0.8,
    "sadness": 0.1,
    "anger": 0.05,
    "fear": 0.05
  }
}
{
  "audio_file": "base64_encoded_audio"
}
curl -X POST https://api.emotwin.ru/v1/analyze/text \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "Ваш текст для анализа"}'
curl -X POST https://api.emotwin.ru/v1/analyze/voice \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"audio_file": "BASE64_ENCODED_AUDIO_DATA"}'
