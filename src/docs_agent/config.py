import os
import yaml
from platformdirs import user_config_dir
from docs_agent.helpers.log import logger

"""Configuration loader for the docs_agent package."""


# Default settings
def defaults():
    return {
        "OLLAMA_URL": "http://localhost:11434",
        "CHAT_MODEL": "llama2",
        "EMBEDDING_MODEL": "nomic-embed-text",
        "OLLAMA_USERNAME": "",
        "OLLAMA_PASSWORD": "",
        "CHROMADB_DIR": ".docs/chromadb",
        "MAX_TOKENS": 4096,
        "SYSTEM_PROMPT": "You are a helpful assistant specialized in providing accurate and concise information based on the provided documentation.",
    }


# Configuration loader
def load_settings_from_file(file_path):
    """Load settings from a YAML file."""
    logger.debug(f"Attempting to load settings from file: {file_path}...")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                cfg = yaml.safe_load(f)
                logger.debug("Settings loaded successfully")
                return cfg if cfg else {}
            except yaml.YAMLError as e:
                logger.error(f"Settings could not be loaded from {file_path}: {e}")
                return {}
    logger.debug(
        f"No config file found at: {file_path}. Using defaults where applicable."
    )
    return {}


def load_config():
    logger.debug("Loading configuration...")
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


def save_config(config):
    """Save the given configuration to the local config file."""
    local_config_path = os.path.join(".docs", "config.yaml")
    logger.debug(f"Attempting to save settings to file: {local_config_path}...")
    with open(local_config_path, "w") as f:
        try:
            yaml.safe_dump(config, f)
            logger.debug("Settings saved successfully")
        except yaml.YAMLError as e:
            logger.error(f"Settings could not be saved to {local_config_path}: {e}")


settings = load_config()


def get_or_set_option(option, value=None):
    """Get or set a configuration option."""
    local_config_path = os.path.join(".docs", "config.yaml")
    local_config = load_settings_from_file(local_config_path)

    if value is not None:
        # Set the option
        local_config[option] = value
        save_config(local_config)
        logger.info(f"Set {option} to {value} in local config.")
    else:
        # Get the option
        if option in local_config:
            logger.info(f"{option} (local): {local_config[option]}")
        elif option in settings:
            logger.info(f"{option} (global/default): {settings[option]}")
        else:
            logger.info(f"{option} is not set.")
