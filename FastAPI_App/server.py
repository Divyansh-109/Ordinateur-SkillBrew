from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from agent import SearchFirstAgent  

app = FastAPI(
    title="Food Recommendation API",
    description="Search-First Food Recommendation Agent using Groq + Serper",
    version="1.0"
)

agent = SearchFirstAgent()

class UserRequest(BaseModel):
    query: str

class FoodRecommendation(BaseModel):
    title: str
    type: str
    platform: str
    reason: str
    rating: float
    link: str
    rating_link: str

class RecommendationResponse(BaseModel):
    status: str
    data: List[FoodRecommendation]

@app.get("/")
def home():
    return {"message": "Food Recommendation API is running"}


@app.post("/recommend", response_model=RecommendationResponse)
def recommend_food(request: UserRequest):
    try:
        result = agent.run(request.query)


        if result is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate recommendations"
            )
        
        if isinstance(result, dict):
            result = [result]

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
