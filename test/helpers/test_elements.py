from docs_agent.helpers.elements import Element

def test_element_creation(with_persistence):
    """
    Tests __init__(), to_dict(), and save() methods of Element class.
    """
    db, manifest_location, _ = with_persistence
    element = Element(name="TestLib", version="1.0", content="This is a test library.", manifest_location=manifest_location, db=db)
    assert element.name == "TestLib"
    assert element.version == "1.0"
    assert element.content == "This is a test library."
    assert element.to_dict() == {
        'ids': "TestLib",
        'metadatas': {"name": "TestLib", "version": "1.0", "updated_at": element.metadata()["updated_at"]},
        'documents': "This is a test library."
    }

    # Test saving to YAML and ChromaDB
    element.save()
    # Check YAML file
    with open(manifest_location, "r", encoding="utf-8") as f:
        data = f.read()
        assert "TestLib" in data
        assert "1.0" in data
    # Check ChromaDB
    results = db.search_elements("TestLib")
    assert "TestLib" in results['ids'][0]
    assert 'This is a test library.' in results['documents'][0]
    assert results['metadatas'][0][0] == {"name": "TestLib", "version": "1.0", "updated_at": element.metadata()["updated_at"]}

def test_element_from_file(with_persistence):
    """
    Tests from_file() method of Element class.
    """
    db, manifest_location, _ = with_persistence
    # Create a YAML file with multiple elements
    import yaml
    elements_data = [
        {"name": "LibA", "version": "1.0", "content": "Content for LibA."},
        {"name": "LibB", "version": "2.0", "content": "Content for LibB."}
    ]
    with open(manifest_location, "w", encoding="utf-8") as f:
        yaml.safe_dump(elements_data, f)

    # Load elements from file
    elements = Element.from_file(manifest_location)
    assert len(elements) == 2
    assert elements[0].name == "LibA"
    assert elements[0].version == "1.0"
    assert elements[0].content == "Content for LibA."
    assert elements[0].to_dict() == {
        'ids': "LibA",
        'metadatas': {"name": "LibA", "version": "1.0", "updated_at": elements[0].metadata()["updated_at"]},
        'documents': "Content for LibA."
    }
    assert elements[1].name == "LibB"
    assert elements[1].version == "2.0"
    assert elements[1].content == "Content for LibB."
    assert elements[1].to_dict() == {
        'ids': "LibB",
        'metadatas': {"name": "LibB", "version": "2.0", "updated_at": elements[1].metadata()["updated_at"]},
        'documents': "Content for LibB."
    }