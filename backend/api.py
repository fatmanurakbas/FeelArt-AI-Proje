from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

PEXELS_API_KEY = 'UKBeHbZZMdf9XENc7wTIwBa2tbqv10VCXULyup6DQiSzxyKvzNWYTXM9'
PEXELS_API_URL = 'https://api.pexels.com/v1/search'

# Anahtar kelime haritası
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

    # Duyguya göre anahtar kelime belirle
    selected_keywords = None
    for emotion, keywords in emotion_keywords.items():
        if emotion in query:
            selected_keywords = keywords
            break

    # Eşleşme yoksa, doğrudan gelen metni kullan
    if not selected_keywords:
        selected_keywords = query

    headers = {
        'Authorization': PEXELS_API_KEY
    }
    params = {
        'query': selected_keywords,
        'per_page': 6
    }

    response = requests.get(PEXELS_API_URL, headers=headers, params=params)

    if response.status_code != 200:
        return jsonify({'error': 'Pexels API hatası'}), 500

    data = response.json()
    image_urls = [photo['src']['medium'] for photo in data.get('photos', [])]

    return jsonify({'images': image_urls})

if __name__ == '__main__':
    print("Flask başlatılıyor...")  # opsiyonel: test çıktısı
    app.run(debug=True)