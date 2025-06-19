import asyncio


from fastapi import Path
from sqlalchemy.orm import Session
from database import get_db
from services.analyse_video import analyze_video_metrics_and_draw
from services.workout_tips import get_applicable_tips  


from pathlib import Path

async def process_video(file_path: str, workout_id: int, db: Session) -> dict:
    loop = asyncio.get_event_loop()
    print(f"Обрабатывается видео для тренировки #{workout_id}")

    output_path = file_path.replace(".mp4", "_processed.mp4")

    metrics = await loop.run_in_executor(None, analyze_video_metrics_and_draw, file_path, output_path)

    tips, completion = get_applicable_tips(db, workout_id, metrics)

    return {
        "tips": tips,
        "completion": 85,
        "processed_video_url": f"tmp/{Path(output_path).name}",
    }
