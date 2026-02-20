import os
import yaml
from platformdirs import user_config_dir
from docs_agent.helpers.log import logger
from dotenv import load_dotenv

"""Configuration loader for the docs_agent package."""

class Config:
    """Configuration class to manage settings for the docs_agent."""
    def __init__(self):
        self.settings = {}
        self.load_config()
    
    @staticmethod
    def from_dict(config_dict):
        """Create a Config instance from a simple dictionary of config values."""
        config = Config()
        for key, value in config_dict.items():
            config.set(key, value, source_desc="from dictionary")
        return config
    
    def __defaults(self):
        return {
            "OLLAMA_URL": {
                "value": "http://localhost:11434",
                "defined_in": "default",
            },
            "CHAT_MODEL": {
                "value": "llama2",
                "defined_in": "default",
            },
            "EMBEDDING_MODEL": {
                "value": "nomic-embed-text",
                "defined_in": "default",
            },
            "OLLAMA_USERNAME": {
                "value": "",
                "defined_in": "default",
            },
            "OLLAMA_PASSWORD": {
                "value": "",
                "defined_in": "default",
            },
            "CHROMADB_DIR": {
                "value": "chromadb",
                "defined_in": "default",
            },
            "MAX_TOKENS": {
                "value": 4096,
                "defined_in": "default",
            },
            "SYSTEM_PROMPT": {
                "value": "You are a helpful assistant specialized in providing accurate and concise information based on the provided documentation.",
                "defined_in": "default",
            },
        }

    def _apply_defaults(self):
        self.settings.update(self.__defaults())

    def _apply_cfg_from_source(self, cfg, source_desc):
        """Normalize and apply config values from a given source."""
        normalized_cfg = {}
        for key, value in cfg.items():
            normalized_cfg[key] = {
                "value": value,
                "defined_in": source_desc,
            }
        self.settings.update(normalized_cfg)
    
    def to_dict(self):
        """Return a simple dict of config values for saving or retrieval."""
        return {k: v["value"] for k, v in self.settings.items()}

    def _load_settings_from_file(self, file_path, source_desc):
        """Load settings from a YAML file."""
        logger.debug(f"Attempting to load settings from file: {file_path}...")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                try:
                    cfg = yaml.safe_load(f)
                    logger.debug("Settings loaded successfully")
                    return self._apply_cfg_from_source(cfg, source_desc) if cfg else {}
                except yaml.YAMLError as e:
                    logger.error(f"Settings could not be loaded from {file_path}: {e}")
                    return {}
        logger.debug(
            f"No config file found at: {file_path}. Using defaults where applicable."
        )
        return {}

    def load_config(self):
        """Load configuration settings from defaults, global config file, local config file, and environment variables."""
        logger.debug("Loading configuration...")
        # First, load default settings
        self._apply_defaults()

        # Second, load global settings
        global_config_path = os.path.join(user_config_dir("docs_agent"), "config.yaml")
        self._load_settings_from_file(global_config_path, "global config file")

        # Third, load local settings
        local_config_path = os.path.join(".docs", "config.yaml")
        self._load_settings_from_file(local_config_path, "local config file")

        # Finally, override with environment variables
        #  Load from `.env` file if it exists
        load_dotenv(dotenv_path=os.path.join(".env"))
        for key in self.__defaults().keys():
            if key in os.environ:
                self.settings[key] = {
                    "value": os.environ[key],
                    "defined_in": "environment variable",
                }
                logger.debug(f"Loaded {key} from environment variable with value: {os.environ[key]}")
        
        # Normalize values
        self.settings["MAX_TOKENS"]["value"] = int(self.settings["MAX_TOKENS"]["value"])
        return self.settings

    def save(self, config_file=os.path.join(".docs", "config.yaml")):
        """Save the given configuration to the local config file."""
        logger.debug(f"Attempting to save settings to file: {config_file}...")
        with open(config_file, "w") as f:
            try:
                yaml.safe_dump(self.to_dict(), f)
                logger.debug("Settings saved successfully")
            except yaml.YAMLError as e:
                logger.error(f"Settings could not be saved to {config_file}: {e}")
    
    def get(self, option):
        """Get the value of a configuration option."""
        return self.settings.get(option, {}).get("value", None)

    def source(self, option):
        """Get the source of a configuration option."""
        return self.settings.get(option, {}).get("defined_in", None)
    
    def set(self, option, value, source_desc="set at runtime"):
        """Set the value of a configuration option."""
        self.settings[option] = {
            "value": value,
            "defined_in": source_desc,
        }

settings = Config()

def get_or_set_option(option, value=None, config_file=os.path.join(".docs", "config.yaml")):
    """Get or set a configuration option."""
    if value is not None:
        source_desc = "local config file"
        settings.set(option, value, source_desc=source_desc)
        settings.save()
        logger.info(f"Set {option} to {value} (in {source_desc}).")
    else:
        # Get the option
        value = settings.get(option)
        if value is not None:
            logger.info(f"{option} (from {settings.source(option)}): {value}")
        else:
            logger.info(f"{option} is not set.")
    return value
