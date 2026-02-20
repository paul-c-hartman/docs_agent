import os
import shutil
import pytest
from docs_agent.setup import main as setup_main

@pytest.mark.skip(reason="Behavior not implemented")
def test_interactive_setup():
    # Setup currently has no interactive steps
    pass

def test_non_interactive_setup():
    """Test that the interactive setup creates the expected directories and files."""
    setup_main(os.path.join(".docs", "test"), non_interactive=False)
    # Check for required directories and files
    assert os.path.exists(".docs/test/.docs"), "Expected .docs directory was not created"
    assert os.path.exists(".docs/test/.docs/config.yaml"), "Expected config.yaml was not created"
    assert os.path.exists(".docs/test/.docs/elements.yaml"), "Expected elements.yaml was not created"
    assert os.path.exists(".docs/test/chromadb"), "Expected ChromaDB directory was not created"

    # Clean up test artifacts
    shutil.rmtree(".docs/test")