from fastapi import FastAPI
from app.db import init_db
from app.schemas import RatingRequest, RatingResponse
from app.llm import predict_rating
from app.db import insert_submission, get_all_submissions
from app.schemas import SubmitReviewRequest, SubmitReviewResponse
from app.llm import generate_ai_outputs
import os
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(
    title="AI Rating Prediction API",
    description="Predicts Yelp star ratings using an LLM",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/predict-rating", response_model=RatingResponse)
def predict_rating_endpoint(request: RatingRequest):
    """
    Predict star rating for a single Yelp review.
    """
    # Let the LLM layer handle failures gracefully
    result = predict_rating(request.review_text)
    return result

@app.post("/submit-review", response_model=SubmitReviewResponse)
def submit_review(payload: SubmitReviewRequest):
    ai_data = generate_ai_outputs(
        payload.rating,
        payload.review
    )

    insert_submission(
        user_rating=payload.rating,
        user_review=payload.review,
        ai_response=ai_data["user_response"],
        ai_summary=ai_data["admin_summary"],
        ai_action=ai_data["recommended_action"]
    )

    return {"message": ai_data["user_response"]}

@app.get("/submissions")
def list_submissions():
    return get_all_submissions()

@app.get("/", include_in_schema=False)
def serve_user_dashboard():
    return FileResponse(
        os.path.join(BASE_DIR, "frontend", "user.html")
    )

@app.get("/admin", include_in_schema=False)
def serve_admin_dashboard():
    return FileResponse(
        os.path.join(BASE_DIR, "frontend", "admin.html")
    )

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "frontend")),
    name="static"
)