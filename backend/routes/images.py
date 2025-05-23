from flask import Flask, request, jsonify
import requests, os, random, uuid
from services.tmdb import get_movies_by_emotion

app = Flask(__name__)

PEXELS_API_KEY = os.getenv("PEXELS_KEY", "UKBeHbZZMdf9XENc7wTIwBa2tbqv10VCXULyup6DQiSzxyKvzNWYTXM9")
PEXELS_API_URL = 'https://api.pexels.com/v1/search'

# Eski `emotion_mapping` ve geniş `emotion_keywords` eklendi
emotion_mapping = {
    "stresli": "sakin", "üzgün": "mutlu", "endişeli": "umutlu", "yalnız": "aşık",
    "korku": "umutlu", "bitkin": "motivasyon", "kararsız": "motivasyon", "öfke": "sakin",
    "kıskanç": "özgüven", "şaşkın": "hayret", "mutlu": "mutlu", "heyecanlı": "mutlu",
    "sakin": "umutlu", "aşık": "romantik", "motivasyon": "başarı",
    "sevinc": "coşku", "hayret": "hayranlık",
}

emotion_keywords = {
    "mutlu": [
        "sunlight in park", "laughing friends", "joyful celebration in nature",
        "colorful balloons in sky", "children playing with kites", "dancing in the rain",
        "happy people hiking", "bright fireworks in open field", "smiling in sunlight"
    ],
    "üzgün": [
        "rainy street at night", "alone with headphones", "dim room with candlelight",
        "tearful eyes", "lonely bench in fog", "gray cloudy sky", 
        "solitary mountain view", "sad painting on wall", "quiet riverbank alone"
    ],
    "stresli": [
        "messy desk with papers", "urban crowd at rush hour", "countdown timer",
        "clocks overlapping", "city chaos from above", "hands holding head in overwhelm",
        "overloaded to-do list", "compressed files on screen", "spilled coffee at work"
    ],
    "sakin": [
        "calm ocean waves", "peaceful forest walk", "zen sand patterns", 
        "open field under blue sky", "soft morning light", 
        "quiet cabin in woods", "mountain lake reflection", "snowflakes falling slowly"
    ],
    "umutlu": [
        "sunrise through trees", "hand reaching toward sky", "flower blooming in rock",
        "light shining through clouds", "new leaf growing", 
        "steps on mountain trail", "open window with fresh breeze", "rainbow after storm"
    ],
    "yalnız": [
        "walking alone by ocean", "shadow on wall alone", "quiet book reading scene",
        "lone tree in snow", "coffee and journal", "solitary bike ride", 
        "evening lights from window", "self-reflection in mirror"
    ],
    "endişeli": [
        "dim hallway with light", "tangled headphones", "clouds rolling in",
        "hand over heart", "anxious eyes close-up", "blurred night lights",
        "abstract tension shapes", "fog covering path"
    ],
    "heyecanlı": [
        "skydiving view", "fireworks over city", "mountain zipline ride",
        "race starting line", "adrenaline adventure", "confetti in air",
        "drone flight over cliffs", "leap into lake", "surprising reveal"
    ],
    "şaşkın": [
        "eyes wide open", "unexpected colors in sky", "first snow on palm",
        "splash frozen in time", "vivid aurora", "magic smoke rising",
        "unusual natural rock", "glowing object in dark", "sparkling mystery"
    ],
    "kızgın": [
        "storm clouds clashing", "cracked ground dry", "abstract red tones",
        "burning match close-up", "exploding paint", "sharp shadows on wall",
        "angry waves crashing", "heat rising from desert"
    ]
}

@app.route('/api/images', methods=['GET'])
def get_images():
    query = request.args.get('query', '').lower().strip()
    if not query:
        return jsonify({'error': 'Sorgu parametresi eksik.'}), 400

    # Duyguyu hedef duyguya çevir
    target_emotion = emotion_mapping.get(query, query)
    keywords = emotion_keywords.get(target_emotion, [target_emotion])
    selected_keyword = random.choice(keywords)

    headers = {'Authorization': PEXELS_API_KEY}
    params = {'query': selected_keyword, 'per_page': 8}

    try:
        response = requests.get(PEXELS_API_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        image_urls = [photo['src']['medium'] for photo in data.get('photos', [])]
        return jsonify({'images': image_urls})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Pexels API hatası: {e}'}), 500
    except Exception as e:
        return jsonify({'error': f'Sunucu hatası: {e}'}), 500

@app.route('/api/recommendations', methods=['GET'])
def api_get_movie_recommendations():
    emotion = request.args.get('emotion', '').lower().strip()
    if not emotion:
        return jsonify({'error': 'Duygu parametresi eksik.'}), 400

    movies = get_movies_by_emotion(emotion)
    if not movies:
        return jsonify({'recommendations': [], 'message': 'Film önerisi bulunamadı.'}), 200
    return jsonify({'recommendations': movies})

@app.route('/recommend', methods=['POST'])
def recommend_movies_post():
    data = request.json
    emotion = data.get('emotion')
    if not emotion:
        return jsonify({'error': 'Emotion not provided in JSON body'}), 400

    processed_emotion = emotion.lower().strip()
    movies = get_movies_by_emotion(processed_emotion)
    if not movies:
        return jsonify({'recommendations': [], 'message': 'Film önerisi bulunamadı.'}), 200
    return jsonify({'recommendations': movies})

if __name__ == '__main__':
    print("Geliştirilmiş Flask API başlatılıyor...")
    app.run(debug=True, port=5000)
