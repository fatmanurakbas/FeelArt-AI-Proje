# backend/routes/images.py
import os, random, httpx, uuid
from fastapi import APIRouter, Query

router = APIRouter()
UNSPLASH_KEY = os.getenv("UNSPLASH_KEY")
PEXELS_KEY = os.getenv("PEXELS_KEY")

# Kullanıcının girdiği duyguya karşılık, onu daha iyi hissettirecek duygu
emotion_mapping = {
    "stresli": "sakin",
    "üzgün": "mutlu",
    "endişeli": "umutlu",
    "yalnız": "aşık",
    "korku": "umutlu",
    "bitkin": "motivasyon",
    "kararsız": "motivasyon",
    "öfke": "sakin",
    "kıskanç": "özgüven",
    "şaşkın": "hayret",
    "mutlu": "mutlu",
    "heyecanlı": "mutlu",
    "sakin": "umutlu",
    "aşık": "romantik",
    "motivasyon": "başarı",
    "sevinc": "coşku",
    "hayret": "hayranlık",
}

# Hedef duygular için anahtar kelime havuzu
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

@router.get("/api/images")
async def images(query: str = Query(...), count: int = 8):
    rng = random.Random(uuid.uuid4().hex)

    # Kullanıcının girdiği duygu → onu rahatlatacak hedef duyguya çevrilir
    target_emotion = emotion_mapping.get(query.lower(), query.lower())
    keywords = emotion_keywords.get(target_emotion, [target_emotion])
    selected_keyword = rng.choice(keywords)

    sources = ["unsplash", "pexels"]
    urls = []

    async with httpx.AsyncClient(timeout=8.0) as client:
        while len(urls) < count and sources:
            src = rng.choice(sources)
            try:
                if src == "unsplash":
                    resp = await client.get(
                        "https://api.unsplash.com/photos/random",
                        params={"query": selected_keyword, "orientation": "landscape", "count": 1},
                        headers={"Authorization": f"Client-ID {UNSPLASH_KEY}"}
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        data = data if isinstance(data, list) else [data]
                        urls.extend([d["urls"]["regular"] for d in data])
                else:
                    resp = await client.get(
                        "https://api.pexels.com/v1/search",
                        params={"query": selected_keyword, "per_page": 10, "page": rng.randint(1, 5)},
                        headers={"Authorization": PEXELS_KEY}
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        rng.shuffle(data["photos"])
                        urls.extend([p["src"]["medium"] for p in data["photos"]])
            except Exception as e:
                print("API error:", e)
            sources.remove(src)

    return {"images": list(dict.fromkeys(urls))[:count]}
