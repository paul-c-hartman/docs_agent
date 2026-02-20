import pytest
import os
import io
from docs_agent.agent import Conversation, ask, chat

if os.getenv("GITHUB_ACTIONS") == "true":
    pytest.skip("Skipping tests that require Ollama server and model in CI environment", allow_module_level=True)

class TestConversation:
    
    def test_conversation_initialization(self):
        """Test that a Conversation object initializes with the correct system prompt and model."""
        conversation = Conversation()
        assert conversation.messages[0]["role"] == "system"
        assert "You are a helpful assistant" in conversation.messages[0]["content"]
        assert conversation.model is not None

    def test_add_user_message(self):
        """Test that add_user_message correctly adds a user message to the conversation."""
        conversation = Conversation()
        conversation.add_user_message("Hello, agent!")
        assert conversation.messages[-1]["role"] == "user"
        assert conversation.messages[-1]["content"] == "Hello, agent!"

    def test_get_response(self):
        """Test that get_response returns a response from the agent."""
        conversation = Conversation()
        conversation.add_user_message("What is the capital of France?")
        response = conversation.get_response()
        assert isinstance(response, str)
        assert len(response) > 0
        assert "Paris" in response

def test_ask():
    """Test the ask function with a simple prompt."""
    response = ask("What is 2 + 2?")
    assert isinstance(response, str)
    assert "4" in response

def test_chat():
    """Test the chat function by simulating a short conversation."""
    in_stream = io.StringIO("What is the capital of Germany?\nWhat about France?\n/done\n")
    out_stream = io.StringIO()
    chat(in_stream=in_stream, out_stream=out_stream)
    output = out_stream.getvalue()
    assert "Berlin" in output
    assert "Paris" in output