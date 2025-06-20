from fastapi import APIRouter, FastAPI, Form, UploadFile, File
from fastapi.responses import JSONResponse
from database import get_db
from services.video_analisis import process_video  # Импортируем функцию обработки видео
from sqlalchemy.orm import Session


router = APIRouter()

from fastapi import Depends

@router.post("/")
async def upload_video(
    file: UploadFile = File(...),
    workout_id: int = Form(...),
    db: Session = Depends(get_db),
):
    file_path = f"/Users/krystsina.karpovich/neurogym_backend/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    result = await process_video(file_path, workout_id, db)

    return JSONResponse(
        content={
            "advice": result["tips"],
            "video_url": result["processed_video_url"],
            "completion": result["completion"],
        }
    )
