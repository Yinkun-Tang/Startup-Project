from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.recommenders import (
    UserBasedCFRecommender, 
    ItemBasedCFRecommender, 
    ContentBasedRecommender, 
    HybridRecommender
)

app = FastAPI(title="Recommender API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user_cf = UserBasedCFRecommender(top_k=10)
item_cf = ItemBasedCFRecommender(top_k=10)
content_cb = ContentBasedRecommender(top_k=10)
hybrid = HybridRecommender(top_k=10, alpha=0.8)

@app.get("/")
async def root():
    return {"message": "Recommender API is running..."}

@app.get("/recommend/{user_id}")
async def recommend(user_id: int):
    try:
        return {
            "user_based_cf": user_cf.recommend(user_id),
            "item_based_cf": item_cf.recommend(user_id),
            "content_based": content_cb.recommend(user_id),
            "hybrid": hybrid.recommend(user_id)
        }
    except KeyError:
        return {
            "user_based_cf": [],
            "item_based_cf": [],
            "content_based": [],
            "hybrid": []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))