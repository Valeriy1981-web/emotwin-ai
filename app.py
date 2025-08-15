# app.py — EmoTwin MVP (Flask + Hugging Face)
from flask import Flask, request, jsonify
from transformers import pipeline
import sqlite3
import os

app = Flask(__name__)

# Загружаем модель анализа эмоций
try:
    sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
except:
    sentiment_pipeline = None

# Инициализация БД
def init_db():
    conn = sqlite3.connect('emotions.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS emotions 
                 (id INTEGER PRIMARY KEY, text TEXT, label TEXT, score REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400

    if sentiment_pipeline:
        result = sentiment_pipeline(text)[0]
        label = result['label']
        score = result['score']
    else:
        label, score = "NEUTRAL", 0.5

    # Сохраняем
    conn = sqlite3.connect('emotions.db')
    c = conn.cursor()
    c.execute("INSERT INTO emotions (text, label, score) VALUES (?, ?, ?)", (text, label, score))
    conn.commit()
    conn.close()

    return jsonify({"label": label, "score": score})

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '').lower()
    
    # Простой логик-ответ на основе ключевых слов
    responses = {
        "грустно": "Раньше ты говорил: «Даже в темноте я находил свет».",
        "устал": "Ты уже прошёл 70% пути. Остановись, но не сдавайся.",
        "не знаю": "Давай вспомним, что ты чувствовал в моменты решений?",
        "скучаю": "Ты оставил много тёплых слов самому себе. Хочешь их услышать?",
    }
    
    for key, resp in responses.items():
        if key in user_input:
            return jsonify({"response": resp})
    
    return jsonify({"response": "Я слышу тебя. Расскажи чуть больше."})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
