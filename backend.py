
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def predict_emotion():
    if "image" not in request.files:
        return jsonify({"error": "Görsel bulunamadı."}), 400
    
    image = request.files["image"]
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    # Burada yapay zeka tahmini yapılacak (şimdilik örnek cevap dönüyoruz)
    result = {"emotion": "mutlu 😊"}  # 👈 örnek sonuç

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
