from .tmdb import get_movies_by_emotion

def get_recommendations(emotion):
    return get_movies_by_emotion(emotion)
