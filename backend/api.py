# api.py (Düzeltilmiş Hali)
from flask import Flask, request, jsonify
import requests
# services.tmdb'den get_movies_by_emotion fonksiyonunu import ediyoruz
from services.tmdb import get_movies_by_emotion

app = Flask(__name__)

# Pexels API Anahtarı ve URL'si
PEXELS_API_KEY = 'UKBeHbZZMdf9XENc7wTIwBa2tbqv10VCXULyup6DQiSzxyKvzNWYTXM9' # API anahtarını güvende tutmayı unutma!
PEXELS_API_URL = 'https://api.pexels.com/v1/search'

# Duygulara karşılık gelen Pexels arama anahtar kelimeleri
emotion_keywords = {
    "mutlu": "joy celebration sunshine vibrant colors",
    "üzgün": "rain dark emotional art lonely",
    "heyecan": "abstract colors energy fireworks",
    "stres": "calm nature peace relaxing",
    "yalnız": "solitude emotional surreal",
    "endişe": "mind therapy breathing nature"
}

@app.route('/api/images', methods=['GET'])
def get_images():
    query = request.args.get('query', '').lower().strip()
    if not query:
        return jsonify({'error': 'Sorgu parametresi eksik.'}), 400

    selected_keywords = None
    for emotion, keywords in emotion_keywords.items():
        if emotion in query: # Kullanıcının girdiği sorguda tanımlı bir duygu varsa
            selected_keywords = keywords
            break
    
    if not selected_keywords: # Eşleşen bir duygu yoksa, direkt sorguyu kullan
        selected_keywords = query

    headers = {
        'Authorization': PEXELS_API_KEY
    }
    params = {
        'query': selected_keywords,
        'per_page': 6  # Örnek olarak 6 görsel
    }

    try:
        response = requests.get(PEXELS_API_URL, headers=headers, params=params)
        response.raise_for_status() # HTTP hatalarını yakala (4xx, 5xx)
        data = response.json()
        image_urls = [photo['src']['medium'] for photo in data.get('photos', [])]
        return jsonify({'images': image_urls})
    except requests.exceptions.RequestException as e:
        print(f"Pexels API isteği hatası: {e}")
        return jsonify({'error': f'Pexels API hatası: {e}'}), 500
    except Exception as e:
        print(f"Görsel işlenirken genel hata: {e}")
        return jsonify({'error': f'Görsel işlenirken sunucuda bir hata oluştu: {e}'}), 500


@app.route('/api/recommendations', methods=['GET'])
def api_get_movie_recommendations(): # Fonksiyon adını değiştirmek, import çakışmalarını önleyebilir
    emotion = request.args.get('emotion', '').lower().strip()
    print(f"API /api/recommendations - Gelen duygu: {emotion}") # Debug için

    if not emotion:
        print("API /api/recommendations - Duygu parametresi eksik.") # Debug için
        return jsonify({'error': 'Duygu parametresi eksik.'}), 400

    movies = get_movies_by_emotion(emotion) # services.tmdb'den çağrı
    print(f"API /api/recommendations - Film listesi: {movies}") # Debug için

    if not movies: # Hem boş liste hem de None kontrolü
        print(f"API /api/recommendations - Film bulunamadı veya geçersiz duygu: {emotion}") # Debug için
        return jsonify({'recommendations': [], 'message': 'Bu duygu için uygun film önerisi bulunamadı.'}), 200 # 404 yerine boş liste ve mesaj dönebiliriz
        # veya return jsonify({'error': 'Film bulunamadı veya geçersiz duygu.'}), 404

    return jsonify({'recommendations': movies})


# Bu route POST metodu ile çalışıyor, farklı bir kullanım senaryosu olabilir.
# Eğer Tkinter'dan GET ile çağırıyorsanız bu route kullanılmıyor demektir.
@app.route('/recommend', methods=['POST'])
def recommend_movies_post(): # Fonksiyon adını değiştirmek
    data = request.json
    emotion = data.get('emotion')
    print(f"API /recommend (POST) - Gelen duygu: {emotion}") # Debug için

    if not emotion:
        print("API /recommend (POST) - Duygu parametresi (JSON body) eksik.") # Debug için
        return jsonify({'error': 'Emotion not provided in JSON body'}), 400

    # Duyguyu küçük harfe çevirip boşlukları temizleyelim
    processed_emotion = emotion.lower().strip()
    movies = get_movies_by_emotion(processed_emotion)
    print(f"API /recommend (POST) - Film listesi: {movies}") # Debug için
    
    if not movies:
        print(f"API /recommend (POST) - Film bulunamadı veya geçersiz duygu: {emotion}") # Debug için
        return jsonify({'recommendations': [], 'message': 'Bu duygu için uygun film önerisi bulunamadı.'}), 200
        # veya return jsonify({'error': 'Film bulunamadı veya geçersiz duygu.'}), 404
        
    return jsonify({'recommendations': movies})

# Flask uygulamasını başlatan tek bir blok olmalı ve tüm route tanımlamalarından sonra gelmeli
if __name__ == '__main__':
    print("Flask backend (api.py) başlatılıyor...")
    app.run(debug=True, port=5000) # Portu belirtmek iyi bir pratiktir