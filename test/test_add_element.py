from docs_agent.add_element import main as add_elements, obtain_text


def test_main():
    """Test the main function of add_element module."""
    # Check that main() correctly adds documentation for a sample tool and source.
    # Here we use a mock or a sample path for testing.
    tools = ["sample_tool"]

    versions = ['0.0.1']
    add_elements(tools=tools, versions=versions, noninteractive=True, silent=False)
    # Check that sample_tool was added to elements.yaml
    with open(".docs/elements.yaml", "r", encoding="utf-8") as f:
        elements_content = f.read()
        assert "sample_tool" in elements_content

def test_obtain_text():
    """Test the obtain_text function with a sample text file."""
    import tempfile
    import os

    # Create a temporary file with some text
    with tempfile.NamedTemporaryFile(
        delete=False, mode="w", encoding="utf-8"
    ) as tmp_file:
        tmp_file.write("Sample documentation text.")
        tmp_file_path = tmp_file.name

    try:
        # Use the obtain_text function to read the file
        text = obtain_text(tmp_file_path)
        assert text == "Sample documentation text."
    finally:
        os.remove(tmp_file_path)  # Clean up the temporary file
