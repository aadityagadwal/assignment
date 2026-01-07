from pathlib import Path

# Path to the prompt file
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "reasons_then_classify.txt"


def get_prompt() -> str:
    """
    Loads and returns the reason-then-classify prompt.
    """
    if not PROMPT_PATH.exists():
        raise FileNotFoundError("Prompt file not found")

    return PROMPT_PATH.read_text()
