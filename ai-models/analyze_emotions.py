import os
import json
import logging
from openai import OpenAI
from typing import Dict, Union

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Улучшенная инициализация клиента OpenAI
def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logging.error("OPENAI_API_KEY не установлен")
        raise ValueError("OPENAI_API_KEY не установлен")
    return OpenAI(api_key=api_key)

client = get_openai_client()

def analyze_text_emotions(text: str) -> Union[Dict[str, float], Dict[str, str]]:
    """
    Анализирует эмоции в тексте через OpenAI API
    
    Args:
        text (str): Текст для анализа
        
    Returns:
        dict: Словарь с уровнями эмоций (0.0-1.0) или сообщение об ошибке
    """
    logging.info(f"Получен текст для анализа длиной {len(text)} символов")
    
    if not text.strip():
        logging.warning("Получен пустой текст")
        return {"error": "Пустой текст"}
    
    # Ограничение длины текста
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
            response_format={"type": "json_object"},
            temperature=0.2
        )
        
        # Обработка ответа
        try:
            result = json.loads(response.choices[0].message.content)
            
            # Проверка корректности ответа
            required_keys = ["joy", "sadness", "anger", "fear", "surprise", "love", "disgust"]
            if not all(key in result for key in required_keys):
                logging.error("Получен некорректный формат ответа от API")
                raise ValueError("Некорректный формат ответа")
            
            logging.info("Успешно получен анализ эмоций")
            return result
            
        except json.JSONDecodeError:
            logging.error("Ошибка парсинга JSON ответа")
            raise ValueError("Ошибка парсинга JSON")
            
    except Exception as e:
        logging.error(f"Произошла ошибка: {str(e)}")
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
