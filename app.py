# app.py — Лёгкая версия EmoTwin (без torch и transformers)
from flask import Flask, request, jsonify
import sqlite3
import os
import random
import tempfile

app = Flask(__name__)

# Исправленный путь к БД
db_path = os.path.join(tempfile.gettempdir(), 'emotions.db')

# Инициализация БД
def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS emotions 
                 (id INTEGER PRIMARY KEY, text TEXT, label TEXT, score REAL, 
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

# Простой "анализ" на основе ключевых слов
def simple_emotion_detector(text):
    text = text.lower()
    positive = ['рад', 'счастье', 'люблю', 'класс', 'отлично', 'круто', 'хорошо', 'свет']
    negative = ['груст', 'плохо', 'ужас', 'ненавижу', 'боль', 'страх', 'тоска', 'одиноко']
    
    pos_count = sum(1 for word in positive if word in text)
    neg_count = sum(1 for word in negative if word in text)
    
    if pos_count > neg_count:
        return "POSITIVE", round(0.5 + random.random() * 0.5, 3)
    elif neg_count > pos_count:
        return "NEGATIVE", round(0.5 + random.random() * 0.5, 3)
    else:
        return "NEUTRAL", round(0.3 + random.random() * 0.4, 3)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data"}), 400
            
        text = data.get('text', '')
        if not text:
            return jsonify({"error": "No text provided"}), 400

        label, score = simple_emotion_detector(text)
        
        # Сохраняем
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("INSERT INTO emotions (text, label, score) VALUES (?, ?, ?)", 
                 (text, label, score))
        conn.commit()
        conn.close()

        return jsonify({"label": label, "score": score})
    
    except Exception as e:
        print(f"Error in /analyze: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if not data or 'message' not in data:
            return jsonify({"error": "Invalid request"}), 400
            
        user_input = data['message'].lower()
        
        responses = {
            "грустно": "Раньше ты говорил: «Даже в темноте я находил свет».",
            "устал": "Ты уже прошёл 70% пути. Остановись, но не сдавайся.",
            "не знаю": "Давай вспомним, что ты чувствовал в моменты решений?",
            "скучаю": "Ты оставил много тёплых слов самому себе. Хочешь их услышать?",
            "рад": "Ты знаешь, как радоваться. Сохрани этот момент.",
            "боюсь": "Страх — это знак, что ты выходишь из зоны комфорта. Это рост."
        }
        
        for key, resp in responses.items():
            if key in user_input:
                return jsonify({"response": resp})
        
        return jsonify({"response": "Я слышу тебя. Расскажи чуть больше."})
    
    except Exception as e:
        print(f"Error in /chat: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port)
