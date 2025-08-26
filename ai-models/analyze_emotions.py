import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_text_emotions(text: str) -> dict:
    """
    Анализирует эмоции в тексте через GPT-4o
    Возвращает словарь с уровнями эмоций (0.0-1.0)
    """
    if not text.strip():
        return {"error": "Пустой текст"}
    
    # Ограничение длины
    max_length = 2000
    truncated_text = text[:max_length] + ("..." if len(text) > max_length else "")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Ты эксперт по анализу эмоций. Оцени текст и верни JSON с уровнями: joy, sadness, anger, fear, surprise, love, disgust. Шкала от 0.0 до 1.0. Никаких дополнительных комментариев."
                },
                {
                    "role": "user",
                    "content": truncated_text
                }
            ],
            response_format={ "type": "json_object" },
            temperature=0.2
        )
        
        # Парсим JSON из ответа
        return json.loads(response.choices[0].message.content)
    
    except Exception as e:
        return {
            "error": str(e),
            "fallback": {
                "joy": 0.0,
                "sadness": 0.0,
                "anger": 0.0,
                "fear": 0.0,
                "surprise": 0.0,
                "love": 0.0,
                "disgust": 0.0
            }
        }
