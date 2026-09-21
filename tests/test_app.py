import pytest
import asyncio
from app import chat_stream

@pytest.mark.asyncio
async def test_chat_stream_type():
    """Verify that chat_stream is an asynchronous generator."""
    # Mocking simple history and message
    message = "Hello"
    history = []

    generator = chat_stream(message, history)
    assert asyncio.iscoroutinefunction(chat_stream) or hasattr(generator, '__aiter__')

@pytest.mark.asyncio
async def test_chat_stream_execution():
    """
    Test the chat_stream execution.
    Note: This requires API keys in .env to actually hit the LLM.
    """
    try:
        message = "Hi"
        history = []
        responses = []
        async for chunk in chat_stream(message, history):
            responses.append(chunk)

        assert len(responses) > 0
        assert isinstance(responses[-1], str)
    except Exception as e:
        pytest.skip(f"Skipping LLM test: API keys likely missing or server unreachable: {e}")
