import requests
from docs_agent.helpers.log import logger


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
            _doc_text = obtain_text(version)
            # Here you would add logic to save doc_text to the appropriate location
            logger.debug(f"Obtained documentation for '{tool}' from '{version}'.")
            if not silent:
                logger.info(
                    f"Successfully added documentation for '{tool}' from '{version}'."
                )
        except Exception as e:
            if not silent:
                logger.error(
                    f"Failed to add documentation for '{tool}' from '{version}': {e}"
                )


def obtain_text(url_or_path):
    """Obtain text from a URL or file path."""
    if url_or_path.startswith("http://") or url_or_path.startswith("https://"):
        response = requests.get(url_or_path)
        response.raise_for_status()
        return response.text
    else:
        with open(url_or_path, "r", encoding="utf-8") as file:
            return file.read()
