import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "submissions.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_rating INTEGER NOT NULL,
            user_review TEXT NOT NULL,
            ai_response TEXT NOT NULL,
            ai_summary TEXT NOT NULL,
            ai_action TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()

def insert_submission(
    user_rating: int,
    user_review: str,
    ai_response: str,
    ai_summary: str,
    ai_action: str
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO submissions
        (user_rating, user_review, ai_response, ai_summary, ai_action, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user_rating,
            user_review,
            ai_response,
            ai_summary,
            ai_action,
            datetime.utcnow().isoformat()
        )
    )

    conn.commit()
    conn.close()

def get_all_submissions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            user_rating,
            user_review,
            ai_response,
            ai_summary,
            ai_action,
            created_at
        FROM submissions
        ORDER BY created_at DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    submissions = []
    for row in rows:
        submissions.append(
            {
                "id": row[0],
                "user_rating": row[1],
                "user_review": row[2],
                "ai_response": row[3],
                "ai_summary": row[4],
                "ai_action": row[5],
                "created_at": row[6]
            }
        )

    return submissions
