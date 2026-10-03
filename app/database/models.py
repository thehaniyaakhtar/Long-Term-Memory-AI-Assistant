# Defining the memories table in Python and creating it in PostgreSQL

# importing the tupes needed to create database columns
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from datetime import datetime, timezone
from app.database.base import Base
# Imports the base class that all database models use

class Memory(Base):
    __tablename__ = "memories"
    
    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, nullable = False)
    memory_text = Column(String, nullable = False)
    memory_type = Column(String, nullable = False)
    importance_score = Column(Integer, nullable = False)
    
    created_at = Column(
        DateTime,
        default = lambda: datetime.now(timezone.utc)
    )
    
    updated_at = Column(
        DateTime,
        default = lambda: datetime.now(timezone.utc),
        onupdate = lambda: datetime.now(timezone.utc)
    )