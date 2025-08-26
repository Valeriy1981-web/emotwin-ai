# EmoTwin AI API Документация

## Базовый URL
`https://api.emotwin.ru/v1`

## Endpoints

### GET /
**Проверка состояния API**  
Возвращает статус и время.

Пример ответа:
```json
{
  "status": "ok",
  "message": "EmoTwin AI API работает!",
  "timestamp": "2024-05-15T12:30:45Z"
}
