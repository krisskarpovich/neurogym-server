from models.workout import ExerciseTip
from sqlalchemy.orm import Session
from database import SessionLocal  # Импортируешь сессию из database.py


def seed_tips(db: Session):
    tips = [
        ExerciseTip(
            workout_id=4,
            condition_key="avg_crunch_angle",
            condition_operator="<",
            condition_value="25",
            message="Недостаточная амплитуда скручивания — попробуйте сильнее сокращать мышцы пресса.",
        ),
        ExerciseTip(
            workout_id=4,
            condition_key="avg_crunch_angle",
            condition_operator=">",
            condition_value="60",
            message="Слишком глубокое скручивание — можно перегрузить позвоночник. Контролируйте движение.",
        ),
        ExerciseTip(
            workout_id=4,
            condition_key="max_body_lean_angle",
            condition_operator=">",
            condition_value="20",
            message="Старайтесь не отклоняться корпусом — держите стабильную позицию.",
        ),
        ExerciseTip(
            workout_id=4,
            condition_key="default",
            condition_operator="==",
            condition_value="true",
            message="Скручивания выполнены технично. Отличная работа!",
        ),
    ]

    db.add_all(tips)
    db.commit()
    print("Советы успешно добавлены!")


if __name__ == "__main__":
    db = SessionLocal()
    seed_tips(db)
    db.close()
