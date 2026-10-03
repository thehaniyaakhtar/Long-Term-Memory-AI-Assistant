# creating an engine to connect to PostgreSQL

from sqlalchemy import create_engine
# the engine that creates a database connection
from sqlalchemy.orm import sessionmaker
# sessionmaker, lets the app create database sessions to interact with PostgreSQL
from dotenv import load_dotenv
# Reads database URL from .env file
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
# Loads the .ebv file and gets the DATABASE_URL

engine = create_engine(DATABASE_URL)
# Creates the database engine

SessionLocal = sessionmaker(
    autocommit = False, # changes arent automatically saved
    autoflush=False,    # SQLAl doesnt automatically send pending changes to db before certain queries
    bind = engine       # which database to use
)
# Creates a session factory called session local