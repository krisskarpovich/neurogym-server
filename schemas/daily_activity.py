from pydantic import BaseModel


class DailyActivitySummary(BaseModel):
    workout_count: int
    total_calories: int
    total_minutes: int
