from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Date, Text
from sqlalchemy.orm import relationship

from database import Base 

class VideoAnalysis(Base):
    __tablename__ = "video_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    exercise_name = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    min_angle = Column(Float)
    max_angle = Column(Float)
    recommendation = Column(Text)

    user = relationship("User")
