import requests

TMDB_API_KEY = "8b4971cb8bd025e788420cabcfc29efb"
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
        print(">>> API başarısız")
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
if __name__ == "__main__":
    movies = get_movies_by_emotion("üzgün")
    print("Test Filmleri:")
    for movie in movies:
        print(movie["title"])




 


