import requests
from docs_agent.helpers.log import logger
from docs_agent.helpers.elements import Element


def main(tools=[], versions=[], noninteractive=False, silent=False):
    """Main add_element function. Invoked by the CLI handler."""

    # For each tool and version, add the element to the local docs.
    # TODO: for now, `version` is a URL/path to the documentation
    for i, tool in enumerate(tools):
        version = versions[i] if i < len(versions) else None
        if not version:
            # TODO: intelligently determine version
            logger.warning(f"No version specified for tool '{tool}'. Skipping.")
            logger.debug("Intelligent version detection not yet implemented.")
            continue
        try:
            # _doc_text = obtain_text(version)
            doc_text = "Text retrieval not yet implemented"
            logger.debug(f"Obtained documentation for '{tool}-{version}'.")
            logger.info(f"Successfully added documentation for '{tool}-{version}'.") if not silent else None
            element = Element(name=tool, version=version, content=doc_text)
            element.save()

        except Exception as e:
            logger.error(f"Failed to add documentation for '{tool}-{version}': {e}") if not silent else None


def obtain_text(url_or_path):
    """Obtain text from a URL or file path."""
    if url_or_path.startswith("http://") or url_or_path.startswith("https://"):
        response = requests.get(url_or_path)
        response.raise_for_status()
        return response.text
    else:
        with open(url_or_path, "r", encoding="utf-8") as file:
            return file.read()
