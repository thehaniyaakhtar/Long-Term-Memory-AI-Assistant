from dotenv import load_dotenv
import os

loaded = load_dotenv()

print("Loaded:", loaded)
print("Value:", repr(os.getenv("DATABASE_URL")))