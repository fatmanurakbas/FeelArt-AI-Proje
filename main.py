from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()  # ← önce bu çalışmalı

# sonra değişkeni oku:
print("UNSPLASH_KEY:", os.getenv("UNSPLASH_KEY"))  # test için
print("PEXELS_KEY:", os.getenv("PEXELS_KEY"))
print("TMDB_KEY:", os.getenv("TMDB_API_KEY"))

app = FastAPI()

from backend.routes import images, recommendation
app.include_router(images.router)
app.include_router(recommendation.router)