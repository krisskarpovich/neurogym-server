import asyncio


# async def process_video(file_path: str, workout_id: int) -> str:

#     print(f"Обрабатывается видео {file_path} для тренировки #{workout_id}")

#     await asyncio.sleep(2)

#     advice = "Сосредоточьтесь на правильной осанке. Позиция спины очень важна."
#     return advice

from sqlalchemy.orm import Session
from database import get_db
from services.analyse_video import analyze_video_metrics
from services.workout_tips import get_applicable_tips  # Depends(get_db) для FastAPI

async def process_video(file_path: str, workout_id: int, db: Session) -> list[str]:
    loop = asyncio.get_event_loop()
    print(f"Обрабатывается видео  для тренировки #{workout_id}")

    # Получаем метрики из видео в отдельном потоке
    metrics = await loop.run_in_executor(None, analyze_video_metrics, file_path)

    # Получаем советы из базы данных по метрикам
    advice = get_applicable_tips(db, workout_id, metrics)
    return advice
