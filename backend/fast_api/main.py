from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import random
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

# Assume backend server runs with provided command in README
movies = pd.read_pickle('data/processed/movies.pkl').set_index('MovieID')
users = pd.read_pickle('data/processed/users.pkl')["UserID"].tolist()

@app.get("/")
async def root():
    return {"message": "Recommender API is running..."}

@app.get("/recommend")
async def recommend(user_id: int = None, random_user: bool = False):
    if random_user or user_id is None:
        user_id = random.choice(users)
    
    recommendations = {
        "UserBasedCF": user_cf.recommend(user_id),
        "ItemBasedCF": item_cf.recommend(user_id),
        "ContentBased": content_cb.recommend(user_id),
        "Hybrid": hybrid.recommend(user_id)
    }
    
    recs_detailed = {}
    for key, mids in recommendations.items():
        recs_detailed[key] = []
        for mid in mids:
            recs_detailed[key].append({
                "MovieID": mid, 
                "Title": movies.loc[mid]["Title"],
                "Genres": movies.loc[mid]["GenresStr"]
            })
    return {
        "UserID": user_id,
        "Recommendations": recs_detailed
    }