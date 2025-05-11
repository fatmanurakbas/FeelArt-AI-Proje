from deepface import DeepFace

def predict_emotion(image_path):
    try:
        result = DeepFace.analyze(
            img_path=image_path,
            actions=['emotion'],
            enforce_detection=False
        )
        
        print("Tüm sonuç:", result)
        print("Duygular:", result[0]["emotion"])
        print("Baskın duygu:", result[0]["dominant_emotion"])

        return {
            "emotion": result[0]["dominant_emotion"],
            "emotions": result[0]["emotion"]
        }
    except Exception as e:
        print("Hata:", e)
        return {"error": str(e)}

