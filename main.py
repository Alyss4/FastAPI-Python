from fastapi import FastAPI
from app.routes import user, task
from init_db import init_db

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API Demo"}

app.include_router(user.router)
app.include_router(task.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
