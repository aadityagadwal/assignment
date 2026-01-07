import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai

from app.prompts import get_prompt


# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in environment")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Use a lightweight, fast model
model = genai.GenerativeModel("models/gemini-2.5-flash")


def predict_rating(review_text: str) -> dict:
    """
    Predicts Yelp star rating for a single review using Gemini.
    Always returns a dictionary with keys:
    - predicted_stars (int)
    - explanation (str)
    """
    try:
        prompt_template = get_prompt()
        final_prompt = prompt_template.replace(
            "{{REVIEW_TEXT}}", review_text[:2000]
        )

        response = model.generate_content(final_prompt)
        raw_text = response.text.strip()

        # Remove markdown fences if present
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()

        # Extract JSON safely
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found in Gemini response")

        parsed = json.loads(match.group())

        # Validate schema
        if not isinstance(parsed.get("predicted_stars"), int):
            raise ValueError("predicted_stars must be an integer")

        if not (1 <= parsed["predicted_stars"] <= 5):
            raise ValueError("predicted_stars out of valid range")

        if not isinstance(parsed.get("explanation"), str):
            raise ValueError("explanation must be a string")

        return parsed

    except Exception as e:
        # Safe fallback — NEVER crash API
        return {
            "predicted_stars": 3,
            "explanation": (
                "The review could not be confidently classified due to "
                "an internal processing issue."
            )
        }
    
def generate_ai_outputs(user_rating: int, user_review: str) -> dict:
    """
    Generates AI responses for user feedback.
    Handles empty reviews gracefully.
    """
    # Handle empty review
    review_text = user_review.strip() if user_review else "(No review text provided)"
    
    try:
        prompt = f"""
You are a customer feedback analysis system.

Input:
Rating: {user_rating}/5
Review: "{review_text}"

Return ONLY valid JSON with no extra text or markdown.

{{
  "user_response": "One friendly sentence replying to the customer",
  "admin_summary": "One concise sentence summarizing the feedback",
  "recommended_action": "One concrete action for the business"
}}
"""

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0,
                "max_output_tokens": 256
            }
        )

        raw = response.text.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()

        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            raise ValueError("Invalid JSON")

        data = json.loads(match.group())

        return {
            "user_response": data.get("user_response", "Thank you for your feedback!"),
            "admin_summary": data.get("admin_summary", f"Customer gave {user_rating}/5 stars."),
            "recommended_action": data.get("recommended_action", "Review feedback manually.")
        }

    except Exception as e:
        # Graceful fallback for any errors
        return {
            "user_response": "Thank you for your feedback!",
            "admin_summary": f"Customer gave {user_rating}/5 stars" + (f": {review_text[:50]}" if review_text != "(No review text provided)" else "."),
            "recommended_action": "Review feedback manually."
        }
