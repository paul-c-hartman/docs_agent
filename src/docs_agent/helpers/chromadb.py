from chromadb import errors, PersistentClient
import os
from typing import Optional

class DB:
    """
    Class to handle interactions with ChromaDB for storing and retrieving documentation elements.
    """

    default_persist_directory = os.path.join(".docs", "chromadb")

    def __init__(self, persist_directory=default_persist_directory):
        self.persist_directory = persist_directory
        # Ensure the directory exists
        os.makedirs(self.persist_directory, exist_ok=True)

    def __chromadb_client(self):
        """Get a ChromaDB client instance."""
        client = PersistentClient(path=self.persist_directory)
        return client

    def __get_collection(self, collection_name):
        """Get or create a ChromaDB collection."""
        client = self.__chromadb_client()
        try:
            collection = client.get_collection(name=collection_name)
        except errors.NotFoundError:
            collection = client.create_collection(name=collection_name)
        return collection

    def get_elements(self):
        """Retrieve all elements from the ChromaDB collection."""
        collection = self.__get_collection("elements")
        return collection.get()

    def search_elements(self, query : str, count : Optional[int] = None):
        """Search for elements in the ChromaDB collection."""
        collection = self.__get_collection("elements")
        count = count if count is not None else max(collection.count(), 1)

        results = collection.query(query_texts=[query], n_results=count)
        return results

    def save_element(self, element):
        """
        Save an element to the ChromaDB collection.
        Update it if it already exists.
        """
        collection = self.__get_collection("elements")
        # Check if element already exists
        existing = collection.query(query_texts=[element.name], n_results=1)
        add_or_update = collection.update if existing['ids'][0] else collection.add
        add_or_update(**element.to_dict())

ChromaDB = DB()