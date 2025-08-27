from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
from datetime import datetime
from typing import Dict
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Константы
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 МБ
UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {".txt", ".mp3", ".wav", ".jpg", ".png"}

app = FastAPI(
    title="EmoTwin AI API",
    description="API для создания эмоционального цифрового двойника",
    version="0.1.0"
)

# Улучшенная настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создание директории для загрузок
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_model=Dict[str, Union[str, datetime]])
def health_check():
    """
    Проверка работоспособности API
    """
    logger.info("Health check выполнен")
    return {
        "status": "ok",
        "message": "EmoTwin AI API работает!",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.
