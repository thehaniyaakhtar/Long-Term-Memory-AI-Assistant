from fastapi import FastAPI

app = FastAPI(
    title = "Long Term Memory AI Assistant"
)

@app.get("/")
def home():
    return{
        "message": "Long-Term Memory AI Assistant is running"
    }