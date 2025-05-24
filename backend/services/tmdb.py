import os
from dotenv import load_dotenv
import requests

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Eksik olan sabit tanımı buraya ekliyoruz:
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/discover/movie"

emotion_to_genre = {
    "mutlu": "35",
    "üzgün": "18",
    "heyecan": "28",
    "stres": "10749",
    "yalnız": "18",
    "endişe": "53"
}

def get_movies_by_emotion(emotion):
    print(f">>> API'den film aranıyor. Duygu: {emotion}")
    genre_id = emotion_to_genre.get(emotion.lower())
    if not genre_id:
        print(">>> Geçersiz duygu, genre bulunamadı.")
        return []

    if not TMDB_API_KEY:
        print(">>> TMDB API anahtarı bulunamadı! .env dosyasını kontrol et.")
        return []

    params = {
        "api_key": TMDB_API_KEY,
        "with_genres": genre_id,
        "sort_by": "popularity.desc",
        "language": "tr-TR",
        "page": 1
    }

    response = requests.get(TMDB_SEARCH_URL, params=params)
    print(f">>> TMDB API status code: {response.status_code}")
    print(f">>> URL: {response.url}")

    if response.status_code != 200:
        print(">>> API başarısız:", response.text)
        return []

    try:
        data = response.json()
        print(">>> API'den dönen veri:", data)
    except Exception as e:
        print(">>> JSON parse hatası:", e)
        return []

    return [
        {
            "title": movie["title"],
            "overview": movie.get("overview", ""),
            "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else ""
        }
        for movie in data.get("results", [])[:5]
    ]

# Test bloğu
if __name__ == "__main__":
    movies = get_movies_by_emotion("üzgün")
    print("Test Filmleri:")
    for movie in movies:
        print(movie["title"])




 


