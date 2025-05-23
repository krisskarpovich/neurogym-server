from models.workout import ExerciseTip
from sqlalchemy.orm import Session

from models.workout import ExerciseTip
from sqlalchemy.orm import Session
from typing import Tuple

from typing import Tuple
from sqlalchemy.orm import Session
from models.workout import ExerciseTip

def get_applicable_tips(db: Session, workout_id: int, metrics: dict) -> Tuple[list[str], float]:
    if not metrics:
        return ["На видео не удалось обнаружить человека. Попробуйте записать повторно."], 0.0

    tips = db.query(ExerciseTip).filter(ExerciseTip.workout_id == workout_id).all()
    
    default_tips = []
    specific_tips = []

    matched_conditions = 0
    total_conditions = 0

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
            total_conditions += 1

            if op == "<" and actual < float(value):
                matched_conditions += 1
                specific_tips.append(tip.message)
            elif op == ">" and actual > float(value):
                matched_conditions += 1
                specific_tips.append(tip.message)
            elif op == "==" and str(actual) == value:
                matched_conditions += 1
                specific_tips.append(tip.message)
        except ValueError:
            continue

    completion_percentage = round((matched_conditions / total_conditions) * 100, 1) if total_conditions > 0 else 0.0

    final_tips = specific_tips if specific_tips else default_tips

    return final_tips, completion_percentage
