from pydantic import BaseModel, Field


class RatingRequest(BaseModel):
    review_text: str = Field(
        ...,
        description="Yelp review text to classify",
        min_length=5
    )


class RatingResponse(BaseModel):
    predicted_stars: int = Field(
        ...,
        description="Predicted star rating (1 to 5)",
        ge=1,
        le=5
    )
    explanation: str = Field(
        ...,
        description="Explanation for the predicted rating"
    )

class SubmitReviewRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    review: str = Field(default="", description="Optional review text")


class SubmitReviewResponse(BaseModel):
    message: str
