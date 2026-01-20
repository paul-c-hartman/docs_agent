"""Sets up the docs agent in your project."""
from docs_agent.config import settings

interactive = True
run_silently = False

def print_silent(*args, **kwargs):
    """Print only if not in silent mode."""
    if not run_silently:
        print(*args, **kwargs)

def ensure_directory(directory="."):
    """Set up the docs agent in the specified directory."""
    import os

    # Create .docs
    docs_dir = os.path.join(directory, ".docs")
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
        print_silent(f"Created directory: {docs_dir}")
    else:
        print_silent(f"Directory already exists: {docs_dir}")

    # Create .docs/config.yaml, .docs/elements.yaml
    config_path = os.path.join(docs_dir, "config.yaml")
    elements_path = os.path.join(docs_dir, "elements.yaml")
    if not os.path.exists(config_path):
        with open(config_path, "w") as f:
            f.write("# Docs agent configuration\n")
        print_silent(f"Created local config file: {config_path}")
    else:
        print_silent(f"Local config file already exists: {config_path}")
    if not os.path.exists(elements_path):
        with open(elements_path, "w") as f:
            f.write("# Languages, libraries, frameworks and tools in use\n")
        print_silent(f"Created local elements file: {elements_path}")
    else:
        print_silent(f"Local elements file already exists: {elements_path}")
    
    # Create ChromaDB directory
    chromadb_dir = os.path.join(directory, settings['CHROMADB_DIR'])
    if not os.path.exists(chromadb_dir):
        os.makedirs(chromadb_dir)
        print_silent(f"Created ChromaDB directory: {chromadb_dir}")
    else:
        print_silent(f"ChromaDB directory already exists: {chromadb_dir}")
    # TODO: agentic project exploration

def main(directory=".", non_interactive=False, silent=False):
    """Main setup function. Invoked by the CLI handler."""
    global interactive, run_silently
    interactive = not non_interactive
    run_silently = silent

    ensure_directory(directory)
    print("Docs agent setup complete.")