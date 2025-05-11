from flask import Flask, request, jsonify
from emotion_analysis.analyzer import predict_emotion

import os

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]

    if not os.path.exists("images"):
        os.makedirs("images")

    image_path = os.path.join("images", image.filename)
    image.save(image_path)

    print("Görsel kaydedildi:", image_path)

    result = predict_emotion(image_path)
    print("Analiz sonucu:", result)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)



