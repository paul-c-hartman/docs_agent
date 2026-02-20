from docs_agent.helpers.elements import Element
from docs_agent.update import main as update_elements
from time import sleep

def test_add_element(with_persistence):
    """Test the main function of update module."""
    db, manifest, _ = with_persistence
    element = Element(name="test_tool", version="0.0.1", content="Initial documentation.", db=db)
    initial_updated_at = element.updated_at
    element.save()

    # Trigger updates
    sleep(1)  # Ensure timestamp will be different after update
    update_elements(force=True, silent=False, verbose=False, db=db, manifest=manifest.as_posix())

    updated_element = db.search_elements("test_tool")
    updated_updated_at = updated_element['metadatas'][0][0]['updated_at']
    assert initial_updated_at != updated_updated_at, "updated_at timestamp should change after update"

def test_needs_update(with_persistence):
    """Test the needs_update function."""
    db, _, _ = with_persistence
    element = Element(name="update_test_tool", version="0.0.1", content="Documentation for update test.", db=db)
    element.save()

    from docs_agent.update import needs_update

    # Test that it does not need update when version is the same
    assert not needs_update("update_test_tool", "0.0.1", db)

    # Test that it needs update when version is different
    assert needs_update("update_test_tool", "0.0.2", db)