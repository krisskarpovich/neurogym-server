from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import (
    activity,
    auth,
    stats,
    workout,
    video_pick,
    workout_results
) 
from database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness Coach API", version="1.0.0")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",  
    "http://127.0.0.1:8080",
    "http://localhost:8080",
    "*", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем маршруты
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(workout.router, prefix="/workouts", tags=["workouts"])
app.include_router(video_pick.router, prefix="/upload", tags=["upload"])
app.include_router(workout_results.router, prefix="/workout_results", tags=["workout_results"])
app.include_router(activity.router, prefix="/activity", tags=["activity"])
app.include_router(stats.router, prefix="/statistics", tags=["statistics"])
app.mount(
    "/uploads",
    StaticFiles(directory="/Users/krystsina.karpovich/neurogym_backend/uploads"),
    name="uploads",
)
app.mount(
    "/tmp",
    StaticFiles(directory="/Users/krystsina.karpovich/neurogym_backend/tmp"),
    name="tmp",
)



@app.get("/")
def read_root():
    return {"message": "Welcome to Fitness Coach API!"}


