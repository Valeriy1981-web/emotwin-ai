# app.py - EmoTwin AI (Production-ready)
from flask import Flask, request, jsonify
from transformers import pipeline
import logging
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Глобальная переменная для модели
sentiment_pipeline = None

@app.before_first_request
def load_model():
    """Загружаем модель при первом запросе"""
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

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "model_loaded": sentiment_pipeline is not None,
        "env": os.environ.get("ENV", "development")
    }), 200

@app.route('/analyze', methods=['POST'])
def analyze():
    """Анализ эмоций в тексте"""
    data = request.get_json()
    if not data or 'text' not in 
        return jsonify({"error": "Поле 'text' обязательно"}), 400

    text = data['text'].strip()
    if not text:
        return jsonify({"error": "Текст не может быть пустым"}), 400

    if not sentiment_pipeline:
        return jsonify({
            "label": "NEUTRAL",
            "score": 0.5,
            "warning": "Модель не загружена, используется заглушка"
        }), 200

    try:
        result = sentiment_pipeline(text)[0]
        label = result['label']
        score = result['score']

        # Нормализуем метки
        label_map = {
            "LABEL_0": "NEGATIVE",
            "LABEL_1": "NEUTRAL",
            "LABEL_2": "POSITIVE"
        }
        normalized_label = label_map.get(label, label)

        return jsonify({
            "label": normalized_label,
            "score": round(score, 4),
            "text_preview": text[:50] + "..." if len(text) > 50 else text
        })
    except Exception as e:
        logger.error(f"Ошибка при анализе: {e}")
        return jsonify({"error": "Не удалось проанализировать текст"}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Чат с EmoTwin (эмоциональный отклик)"""
    data = request.get_json()
    if not data or 'message' not in 
        return jsonify({"error": "Поле 'message' обязательно"}), 400

    message = data['message'].lower().strip()

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
            return jsonify({"response": response})

    return jsonify({
        "response": "Я слышу тебя. Расскажи чуть больше — я хочу понять."
    })

if __name__ == '__main__':
    # Важно: bind to 0.0.0.0 and use PORT env var
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"Запуск сервера на порту {port}")
    app.run(host='0.0.0.0', port=port)
