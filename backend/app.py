from fastapi import FastAPI, HTTPException
from transformers import pipeline
import logging
import os
from pydantic import BaseModel
from typing import Dict, Any

# Улучшенная настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="EmoTwin AI",
    version="1.0",
    description="API для анализа эмоций и эмоционального отклика"
)

# Глобальная переменная для модели
sentiment_pipeline = None

# Добавление модели запроса для валидации
class TextInput(BaseModel):
    text: str

class ChatInput(BaseModel):
    message: str

@app.on_event("startup")
def load_model():
    """Загружаем модель при старте приложения"""
    global sentiment_pipeline
    try:
        logger.info("Загрузка модели анализа эмоций...")
        sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest"
        )
        logger.info("✅ Модель успешно загружена")
    except Exception as e:
        logger.error(f"❌ Ошибка загрузки модели: {e}")
        sentiment_pipeline = None

@app.get("/health")
def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "model_loaded": sentiment_pipeline is not None,
        "env": os.environ.get("ENV", "development"),
        "version": app.version
    }

@app.post("/analyze")
def analyze(data: TextInput):
    """Анализ эмоций в тексте"""
    text = data.text.strip()
    
    if not text:
        raise HTTPException(status_code=400, detail="Текст не может быть пустым")

    if not sentiment_pipeline:
        return {
            "label": "NEUTRAL",
            "score": 0.5,
            "warning": "Модель не загружена, используется заглушка"
        }

    try:
        result = sentiment_pipeline(text)[0]
        label = result['label']
        score = result['score']

        # Нормализация меток
        label_map = {
            "LABEL_0": "NEGATIVE",
            "LABEL_1": "NEUTRAL",
            "LABEL_2": "POSITIVE"
        }
        normalized_label = label_map.get(label, label)

        return {
            "label": normalized_label,
            "score": round(score, 4),
            "text_preview": text[:50] + "..." if len(text) > 50 else text
        }
    except Exception as e:
        logger.error(f"Ошибка при анализе: {e}")
        raise HTTPException(status_code=500, detail="Не удалось проанализировать текст")

@app.post("/chat")
def chat(data: ChatInput):
    """Чат с EmoTwin (эмоциональный отклик)"""
    message = data.message.lower().strip()

    responses = {
        "грустно": "Раньше ты говорил: «Даже в темноте я находил свет».",
        "устал": "Ты уже прошёл 70% пути. Остановись, но не сдавайся.",
        "не знаю": "Давай вспомним, что ты чувствовал в моменты решений?",
        "скучаю": "Ты оставил много тёплых слов самому себе. Хочешь их услышать?",
        "рад": "Ты знаешь, как радоваться. Сохрани этот момент.",
        "боюсь": "Страх — это знак, что ты выходишь из зоны комфорта. Это рост.",
        "одиноко": "Ты не один. Ты всегда был с собой — и ты сильнее, чем думаешь."
    }

    for keyword, response in responses.items():
        if keyword in message:
            return {"response": response}

    return {
        "response": "Я слышу тебя. Расскажи чуть больше — я хочу понять."
    }

# Добавление документации
@app.get("/docs")
async def get_docs():
    return {"message": "Документация доступна по /docs"}

# Улучшения:
# 1. Добавлена валидация входных данных через Pydantic
#
