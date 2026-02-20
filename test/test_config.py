from docs_agent.config import Config, get_or_set_option
import os
import yaml

def test_load_config():
    """Test that load_config returns a dictionary with expected keys."""
    config = Config()
    assert isinstance(config.to_dict(), dict)
    expected_keys = {"MAX_TOKENS": int, "OLLAMA_URL": str, "CHAT_MODEL": str, "EMBEDDING_MODEL": str, "SYSTEM_PROMPT": str, "OLLAMA_USERNAME": str, "OLLAMA_PASSWORD": str, "CHROMADB_DIR": str}
    for key, expected_type in expected_keys.items():
        assert key in config.to_dict(), f"Expected key '{key}' not found in config"
        assert isinstance(config.get(key), expected_type), f"Expected type {expected_type} for key '{key}', got {type(config.to_dict()[key])}"

def test_save_config(with_persistence):
    """Test that save_config correctly saves a config dictionary to the local config file."""
    _, _, config_path = with_persistence
    test_config = {
        "MAX_TOKENS": 2048,
        "OLLAMA_URL": "http://localhost:11434",
        "CHAT_MODEL": "test-model",
        "EMBEDDING_MODEL": "test-embedding-model",
        "SYSTEM_PROMPT": "You are a test assistant."
    }
    config = Config.from_dict(test_config)
    config.save(config_path.as_posix())
    assert os.path.exists(config_path.as_posix()), "Config file was not created"
    with open(config_path.as_posix(), "r") as f:
        loaded_config = yaml.safe_load(f)
    for key in test_config.keys():
        assert key in loaded_config, f"Expected key '{key}' not found in saved config"
        assert loaded_config[key] == test_config[key], f"Expected value '{test_config[key]}' for key '{key}', got '{loaded_config[key]}'"

def test_get_or_set_option(with_persistence):
    """Test that get_or_set_option retrieves existing options and sets new ones."""
    _, _, config_path = with_persistence
    # Test setting a new option
    value = get_or_set_option("TEST_OPTION", "default_value", config_path.as_posix())
    assert value == "default_value", f"Expected 'default_value', got '{value}'"
    # Test retrieving the existing option
    value = get_or_set_option("TEST_OPTION", None, config_path.as_posix())
    assert value == "default_value", f"Expected 'default_value', got '{value}'"