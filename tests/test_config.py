import pytest
from Avora import VOICE_INSTRUCTIONS, CHAT_INSTRUCTIONS, MODEL_ID

def test_prompts_exist():
    """Ensure system prompts are defined and not empty."""
    assert VOICE_INSTRUCTIONS is not None
    assert len(VOICE_INSTRUCTIONS) > 0
    assert CHAT_INSTRUCTIONS is not None
    assert len(CHAT_INSTRUCTIONS) > 0

def test_prompt_distinction():
    """Ensure voice and chat prompts are different for their respective roles."""
    assert VOICE_INSTRUCTIONS != CHAT_INSTRUCTIONS
    # Voice should be concise, Chat should be professional/markdown
    assert "concise" in VOICE_INSTRUCTIONS.lower()
    assert "markdown" in CHAT_INSTRUCTIONS.lower()

def test_model_config():
    """Ensure the model ID is correctly set."""
    assert MODEL_ID == "google/gemma-4-31b-it"
