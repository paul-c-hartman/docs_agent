import ollama
import functools
import time
from docs_agent.config import settings
from docs_agent.helpers.filesize import filesize_to_english
from docs_agent.helpers.log import logger


def _is_model_available(client, model_name):
    """Check if a model is available locally."""
    models = [model["model"] for model in client.list()["models"]]
    model_name = f"{model_name}:latest" if ":" not in model_name else model_name
    model_available = model_name in models
    logger.debug(f"Model availability for '{model_name}': {model_available}")
    return model_available


@functools.cache  # Initialize client only once
def init_client():
    """Initialize Ollama client and ensure models are available."""
    config = settings
    ollama_url = config.get("OLLAMA_URL")
    logger.debug(f"Initializing Ollama at {ollama_url}...")
    ollama_client = ollama.Client(host=ollama_url, timeout=2.0)
    # Ensure models are available
    chat_model = config.get("CHAT_MODEL")
    embedding_model = config.get("EMBEDDING_MODEL")
    for model in [chat_model, embedding_model]:
        if _is_model_available(ollama_client, model):
            logger.debug(f"Model '{model}' is already available. Skipping pull.")
            continue
        logger.info(f"Pulling model '{model}' from Ollama server...")
        try:
            max_length = 0
            for status in ollama_client.pull(model, stream=True):
                status_line = f"\rStatus: {status.get('status')}, Completed: {filesize_to_english(status.get('completed'))}/{filesize_to_english(status.get('total'))} ({(status.get('completed') or 0) / (status.get('total') or 1) * 100:.2f}%)"
                max_length = max(max_length, len(status_line))
                status_line = status_line.ljust(max_length)
                print(status_line, end="", flush=True)
                time.sleep(0.5)
            logger.info(f"\nSuccessfully pulled model: {model}")
        except Exception as e:
            logger.error(f"\nAn error occurred while pulling the model: {e}")
            raise e
    return ollama_client, config


class Conversation:
    """
    Conversation class for managing chat sessions with the docs agent.
    """

    def __init__(self, system_prompt=None, model=None, **kwargs):
        """Creates a conversation. Optionally specify a system prompt and model. Additional arguments are passed directly to the Ollama client."""
        self.client, self.config = init_client()
        system_prompt = system_prompt or self.config.get("SYSTEM_PROMPT")
        self.messages = [{"role": "system", "content": system_prompt}]
        self.model = model or self.config.get("CHAT_MODEL")
        self.args = kwargs

    def add_user_message(self, content):
        self.messages.append({"role": "user", "content": content})

    def get_response(self):
        response = self.client.chat(
            model=self.model, messages=self.messages, **self.args
        )
        self.messages.append(
            {"role": "assistant", "content": response.message["content"]}
        )
        return response.message["content"]

    def stream_response(self):
        self.messages.append({"role": "assistant", "content": ""})
        for chunk in self.client.chat(
            model=self.model, messages=self.messages, stream=True, **self.args
        ):
            self.messages[-1]["content"] += chunk.message["content"]
            yield chunk.message["content"]


def ask(prompt="", stream=False):
    """
    Ask function for the docs agent. Invoked by the CLI handler.
    Supports streaming responses.
    """
    conversation = Conversation()
    conversation.add_user_message(prompt)
    if stream:
        logger.debug("Streaming response...")
        for chunk in conversation.stream_response():
            print(chunk, end="", flush=True)
        print()  # Newline after streaming
    else:
        logger.debug("Getting full response...")
        response = conversation.get_response()
        logger.debug("Got response:")
        print(response)


def chat():
    """Chat function for the docs agent. Invoked by the CLI handler."""
    conversation = Conversation()
    logger.info("Starting chat session with the Docs agent. Type '/done' to quit.")
    while True:
        user_input = input("> ")
        if user_input.strip().lower() == "/done":
            logger.info("Ending chat session.")
            break
        conversation.add_user_message(user_input)
        for chunk in conversation.stream_response():
            print(chunk, end="", flush=True)
        print()  # Newline after streaming
        print()  # Extra newline for readability
