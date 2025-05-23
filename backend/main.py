from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()  # ← önce bu çalışmalı

# sonra değişkeni oku:
print("UNSPLASH_KEY:", os.getenv("UNSPLASH_KEY"))  # test için
print("PEXELS_KEY:", os.getenv("PEXELS_KEY"))

app = FastAPI()

from routes import images
app.include_router(images.router)
