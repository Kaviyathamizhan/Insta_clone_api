from fastapi import FastAPI
from routers import posts
from fastapi.responses import JSONResponse

app = FastAPI(title="InstaClone API", version="1.0")
app.include_router(posts.router)

@app.get("/")
def home():
    return JSONResponse({"message": "Welcome to InstaClone API!"})
