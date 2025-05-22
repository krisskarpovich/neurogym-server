from models.workout import ExerciseTip
from sqlalchemy.orm import Session

def get_applicable_tips(db: Session, workout_id: int, metrics: dict) -> list[str]:
    tips = db.query(ExerciseTip).filter(ExerciseTip.workout_id == workout_id).all()
    
    default_tips = []
    specific_tips = []

    for tip in tips:
        key = tip.condition_key
        op = tip.condition_operator
        value = tip.condition_value

        if key == "default":
            default_tips.append(tip.message)
            continue

        actual = metrics.get(key)
        if actual is None:
            continue

        try:
            if op == "<" and actual < float(value):
                specific_tips.append(tip.message)
            elif op == ">" and actual > float(value):
                specific_tips.append(tip.message)
            elif op == "==" and str(actual) == value:
                specific_tips.append(tip.message)
        except ValueError:
            continue

    # Если есть конкретные советы, не показываем дефолтные
    if specific_tips:
        return specific_tips
    return default_tips

