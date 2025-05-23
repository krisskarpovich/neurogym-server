import asyncio


from sqlalchemy.orm import Session
from database import get_db
from services.analyse_video import analyze_video_metrics
from services.workout_tips import get_applicable_tips  


async def process_video(file_path: str, workout_id: int, db: Session) -> list[str]:
    loop = asyncio.get_event_loop()
    print(f"Обрабатывается видео  для тренировки #{workout_id}")

    metrics = await loop.run_in_executor(None, analyze_video_metrics, file_path)

    tips, completion = get_applicable_tips(db, workout_id, metrics)

    return {
        "tips": tips,
        "completion": completion,  
    }
