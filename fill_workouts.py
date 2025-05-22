# fill_workouts.py
from sqlalchemy.orm import Session
from database import get_db
from models.workout import Workout

def fill_workouts():
    db = next(get_db())  # Создаем сессию для работы с базой данных

    try:
        workouts_data = [
            {
                "logo_url": "https://example.com/logo1.png",
                "exercise_type": "Push-up",
                "instructions": "1. Get into plank position. 2. Lower your body and push back up.",
                "image_url": "https://example.com/pushup.png"
            },
            {
                "logo_url": "https://example.com/logo2.png",
                "exercise_type": "Squat",
                "instructions": "1. Stand with feet shoulder-width apart. 2. Lower your hips and return to standing.",
                "image_url": "https://example.com/squat.png"
            },
        ]

        for workout_data in workouts_data:
            workout = Workout(
                logo_url=workout_data["logo_url"],
                exercise_type=workout_data["exercise_type"],
                instructions=workout_data["instructions"],
                image_url=workout_data["image_url"]
            )
            db.add(workout)

        db.commit()
        print("Workouts have been added successfully!")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()

    finally:
        db.close()

if __name__ == "__main__":
    fill_workouts()
