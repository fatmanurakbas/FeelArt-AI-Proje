import requests

API_KEY = "8b4971cb8bd025e788420cabcfc29efb"
BASE_URL = "https://api.themoviedb.org/3"

# Duyguyu film türüne çevir
emotion_to_genre = {
    "mutlu": "35",         # Komedi
    "üzgün": "18",         # Dram
    "heyecan": "28",       # Aksiyon
    "stres": "10749",      # Romantik (ya da rahatlatıcı temalar)
    "yalnız": "18",        # Dram (ya da romantik olabilir)
    "endişe": "53",        # Gerilim
}


def get_movies_by_emotion(emotion):
    genre_id = emotion_to_genre.get(emotion.lower())
    if not genre_id:
        return []

    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "with_genres": genre_id,
        "sort_by": "popularity.desc",
        "language": "tr-TR"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])[:5]
    return []
