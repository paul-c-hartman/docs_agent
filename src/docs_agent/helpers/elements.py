from docs_agent.helpers.chromadb import ChromaDB, DB
from datetime import datetime

class Element:
    """
    Class representing a documentation element: a language, tool, framework, or library.
    Also holds version info and handles save/load.
    """
    
    default_manifest_location = ".docs/elements.yaml"
    default_db = ChromaDB

    def __init__(self, name: str, version: str, content: str, manifest_location: str = default_manifest_location, db: DB = default_db):
        self.name = name
        self.version = version
        self.content = content
        self.manifest_location = manifest_location
        self.db = db
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self):
        """
        Convert the element to a dictionary format suitable for saving to YAML or ChromaDB.
        """
        return {
            'ids': self.name,
            'metadatas': {
                "name": self.name,
                "version": self.version,
                "updated_at": self.updated_at
            },
            'documents': self.content,
            # 'embeddings': [[0.0]*1536] # TODO: document embeddings
        }

    def metadata(self):
        """
        Return just the metadata for this element.
        """
        return self.to_dict()['metadatas']
    
    def save(self):
        self.save_yaml()
        self.db.save_element(self)
    
    def save_yaml(self):
        import yaml
        # First read file if it exists
        try:
            with open(self.manifest_location, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        except FileNotFoundError:
            data = {}
        # Append new element
        data.update(self.metadata())  # Use metadata for YAML storage
        # Write back to file
        with open(self.manifest_location, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f)

    def __repr__(self):
        return f"Element(name={self.name}, version={self.version})"
    
    @staticmethod
    def from_file(filepath: str):
        import yaml
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or []
        return [Element(name=item["name"], version=item["version"], content=item["content"]) for item in data]