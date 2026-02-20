from docs_agent.helpers.chromadb import DB
from docs_agent.helpers.elements import Element

def test_db_initialization(with_persistence):
    """
    Tests initialization of ChromaDB class and its methods.
    """
    db, _, _ = with_persistence
    assert isinstance(db, DB)

def test_get_elements(with_persistence):
    """
    Tests get_elements() method of ChromaDB class.
    """
    db, _, _ = with_persistence
    elements = db.get_elements()
    assert isinstance(elements, dict)
    assert 'ids' in elements
    assert 'metadatas' in elements
    assert 'documents' in elements

def test_search_elements(with_persistence):
    """
    Tests search_elements() method of ChromaDB class.
    """
    db, _, _ = with_persistence
    # Add a test element to the collection
    test_element = Element(name="TestElement", version="1.0", content="This is a test element.")
    db.save_element(test_element)

    # Search for the test element
    results = db.search_elements("TestElement")
    assert isinstance(results, dict)
    assert "TestElement" in results['ids'][0]
    assert 'This is a test element.' in results['documents'][0]
    assert results['metadatas'][0][0] == {"name": "TestElement", "version": "1.0", "updated_at": test_element.metadata()["updated_at"]}

def test_save_element(with_persistence):
    """
    Tests save_element() method of ChromaDB class.
    """
    db, _, _ = with_persistence
    test_element = Element(name="SaveTest", version="1.0", content="Testing save_element method.")
    db.save_element(test_element)

    # Verify element was saved
    results = db.search_elements("SaveTest")
    assert "SaveTest" in results['ids'][0]
    assert 'Testing save_element method.' in results['documents'][0]
    assert results['metadatas'][0][0] == {"name": "SaveTest", "version": "1.0", "updated_at": test_element.metadata()["updated_at"]}