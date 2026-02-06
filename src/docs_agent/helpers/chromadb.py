from chromadb import errors, PersistentClient
import os
from typing import Optional

persist_directory = os.path.join(".docs", "chromadb")

def get_chromadb_client():
    """Get a ChromaDB client instance."""
    client = PersistentClient(path=persist_directory)
    return client

def get_collection(collection_name):
    """Get or create a ChromaDB collection."""
    client = get_chromadb_client()
    try:
        collection = client.get_collection(name=collection_name)
    except errors.NotFoundError:
        collection = client.create_collection(name=collection_name)
    return collection

def get_elements():
    """Retrieve all elements from the ChromaDB collection."""
    collection = get_collection("elements")
    return collection.get()

def search_elements(query, count : Optional[int] = None):
    """Search for elements in the ChromaDB collection."""
    collection = get_collection("elements")
    count = count if count is not None else collection.count()

    results = collection.query(query_texts=[query], n_results=count)
    return results

def save_element(element):
    """
    Save an element to the ChromaDB collection.
    Update it if it already exists.
    """
    collection = get_collection("elements")
    # Check if element already exists
    existing = collection.query(query_texts=[element.name], n_results=1)
    add_or_update = collection.update if existing['ids'][0] else collection.add
    add_or_update(
        ids=[existing['ids'][0][0]] or [element.name],
        metadatas=[{
            "name": element.name,
            "version": element.version
        }],
        documents=[element.content],
        embeddings=[[0.0]*1536]  # Placeholder embedding
    )