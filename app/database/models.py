# Defining the memoties table in Python and creating it in PostgreSQL
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from datetime import datetime
from app.database.base import Base

class Memory(Base):
    __tablename__ = "memories"
    
    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, nullable = False)
    memory_text = Column(String, nullable = False)
    memory_type = Column(String, nullable = False)
    importance_score = Column(Integer, nullable = False)
    
    created_at = Column(
        DateTime,
        default = datetime.utcnow
    )
    
    updated_at = Column(
        DateTime,
        default = datetime.utcnow,
        onupdate = datetime.utcnow
    )