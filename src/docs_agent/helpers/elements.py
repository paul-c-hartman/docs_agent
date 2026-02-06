from docs_agent.helpers.chromadb import save_element

class Element:
    """
    Class representing a documentation element: a language, tool, framework, or library.
    Also holds version info and handles save/load.
    """
    
    manifest_location = ".docs/elements.yaml"

    def __init__(self, name: str, version: str, content: str):
        self.name = name
        self.version = version
        self.content = content
        
    
    def to_dict(self):
        return {
            self.name: {
                "version": self.version,
                "content": self.content
            }
        }
    
    def save(self):
        import yaml
        # First read file if it exists
        try:
            with open(self.manifest_location, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        except FileNotFoundError:
            data = {}
        # Append new element
        data.update(self.to_dict())
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