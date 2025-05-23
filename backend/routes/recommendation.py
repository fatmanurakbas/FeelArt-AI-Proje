from fastapi import APIRouter, Query, Body
from backend.services.recommendation_service import get_recommendations

router = APIRouter()

# GET yöntemi ile film önerisi (örnek: /api/recommendations?emotion=mutlu)
@router.get("/api/recommendations")
def recommend_movies(emotion: str = Query(..., description="Kullanıcının girdiği duygu")):
    print(f"Gelen duygu: {emotion}")
    movies = get_recommendations(emotion.lower().strip())
    if not movies:
        return {"recommendations": [], "message": "Bu duygu için uygun film önerisi bulunamadı."}
    return {"recommendations": movies}

# POST yöntemi ile film önerisi (örnek: JSON body ile gönderim)
@router.post("/recommend")
def recommend_movies_post(data: dict = Body(...)):
    emotion = data.get("emotion", "").strip().lower()
    print(f"POST isteğiyle gelen duygu: {emotion}")
    if not emotion:
        return {"error": "Emotion not provided"}
    movies = get_recommendations(emotion)
    if not movies:
        return {"recommendations": [], "message": "Film bulunamadı"}
    return {"recommendations": movies}
