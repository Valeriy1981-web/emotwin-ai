from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
from datetime import datetime

app = FastAPI(
    title="EmoTwin AI API",
    description="API для создания эмоционального цифрового двойника",
    version="0.1.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Папка для загрузок
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "EmoTwin AI API работает!",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/v1/upload")
async def upload_user_data(file: UploadFile = File(...)):
    """
    Загружает пользовательские данные для анализа эмоций
    Поддерживает: .txt, .mp3, .wav, .jpg, .png
    """
    # Проверка расширения
    allowed_extensions = {".txt", ".mp3", ".wav", ".jpg", ".png"}
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Неподдерживаемый формат. Допустимые: {', '.join(allowed_extensions)}"
        )
    
    # Генерация уникального имени
    safe_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    # Сохранение файла
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    return {
        "filename": file.filename,
        "stored_as": safe_filename,
        "size": f"{os.path.getsize(file_path)} bytes",
        "upload_time": datetime.utcnow().isoformat(),
        "message": "Файл успешно загружен. Анализ начнётся в течение 5 минут."
    }
