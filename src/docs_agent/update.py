from docs_agent.helpers.log import logger

from docs_agent.helpers.elements import Element
from docs_agent.helpers.chromadb import ChromaDB

def needs_update(name, version, db):
    """Check if an element needs updating."""
    element = db.search_elements(name)
    # TODO: check if version is up to date, integrating with intelligent version retrieval with `add_element`
    if element['metadatas'][0][0]['version'] == version:
        return False  # No need to update if already exists with same version
    return True  # Needs update if not found or different version

def main(force=False, silent=False, verbose=False, db=ChromaDB, manifest=".docs/elements.yaml"):
    """Main update function. Invoked by the CLI handler."""
    elements = db.get_elements()
    for element in elements['metadatas'] or []:
        name = str(element['name'])
        version = str(element['version'])
        if needs_update(name, version, db) or force:
            logger.info(f"Updating documentation for '{name}-{version}'...") if not silent else None
            try:
                # doc_text = obtain_text(name, version)
                doc_text = "Text retrieval not yet implemented"
                logger.debug(f"Obtained updated documentation for '{name}-{version}'.")
                updated_element = Element(name=name, version=version, content=doc_text, db=db)
                updated_element.save()
                logger.info(f"Successfully updated documentation for '{name}-{version}'.") if not silent else None
            except Exception as e:
                logger.error(f"Failed to update documentation for '{name}-{version}': {e}") if not silent else None
        else:
            logger.info(f"Documentation for '{name}-{version}' is already up to date.") if not silent else None
