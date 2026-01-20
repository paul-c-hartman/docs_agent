"""Configuration loader for the docs_agent package."""

# Default settings
def defaults():
    return {
        "OLLAMA_URL": "http://localhost:11434",
        "CHAT_MODEL": "llama2",
        "EMBEDDING_MODEL": "text-embedding-3-small",
        "OLLAMA_USERNAME": "",
        "OLLAMA_PASSWORD": "",
        "CHROMADB_DIR": ".docs/chromadb",
        "MAX_TOKENS": 4096,
    }

# Configuration loader
import os
import yaml
from platformdirs import user_config_dir
from docs_agent import __version__

def load_settings_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    return {}

def load_config():
    # First, load default settings
    config = defaults()

    # Second, load global settings
    global_config_path = os.path.join(user_config_dir("docs_agent"), "config.yaml")
    config.update(load_settings_from_file(global_config_path))
    
    # Third, load local settings
    local_config_path = os.path.join(".docs", "config.yaml")
    config.update(load_settings_from_file(local_config_path))

    # Finally, override with environment variables
    for key in defaults().keys():
        if key in os.environ:
            config[key] = os.environ[key]
    return config

settings = load_config()