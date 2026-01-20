"""Sets up the docs agent in your project."""
from docs_agent.config import settings

def ensure_directory(directory="."):
    """Set up the docs agent in the specified directory."""
    import os

    # Create .docs
    docs_dir = os.path.join(directory, ".docs")
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)

    # Create .docs/config.yaml, .docs/elements.yaml
    config_path = os.path.join(docs_dir, "config.yaml")
    elements_path = os.path.join(docs_dir, "elements.yaml")
    if not os.path.exists(config_path):
        with open(config_path, "w") as f:
            f.write("# Docs agent configuration\n")
    if not os.path.exists(elements_path):
        with open(elements_path, "w") as f:
            f.write("# Languages, libraries, frameworks and tools in use\n")
    
    # Create ChromaDB directory
    chromadb_dir = os.path.join(directory, settings['CHROMADB_DIR'])
    if not os.path.exists(chromadb_dir):
        os.makedirs(chromadb_dir)

def main(directory="."):
    """Main setup function."""
    ensure_directory(directory)
    print("Docs agent setup complete.")