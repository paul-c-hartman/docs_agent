"""
Docs agent.

Usage:
  docs init [<dir>] [(-i | --interactive) | (-n | --non-interactive [--silent])]
  docs add (<tool> [<version>]) ... [(-i | --interactive) | (-n | --non-interactive [--silent])] [--verbose]
  docs config <option> [<value>]
  docs ask [--stream] [--] <prompt>
  docs chat
  docs (pull | update) [--force] [--silent | --verbose]
  docs -h | --help
  docs -v | --version

Commands:
  init [<dir>]                 Initialize and configure the docs agent for your project. Uses the current directory if none is specified. Creates and sets up the .docs folder if it doesn't exist.
  add (<tool> [<version>])...  Manually add one or more tools, languages, or libraries to your local docs.
  config <option> [<value>]    If a value is given, sets the configuration option to that value, assuming `--local` if neither `--local` or `--global` is specified. If a value is not given, reports the existing configuration for that value and where it came from (global or local config).
  ask <prompt>                 Ask the Docs agent a question. Response can be streamed with `--stream`.
  chat                         Start a chat session with the Docs agent.
  pull | update                Check for version updates and re-pull documentation where necessary.

Options:
  -h, --help                   Show this screen.
  -v, --version                Show version.
  -i, --interactive            Configure project interactively. Runs interactively by default.
  -n, --non-interactive        Configure project noninteractively, e.g. for scripts. Uses sensible defaults.
  --silent                     Configure project silently. Must be used with `--non-interactive`.
  --verbose                    Configure progress verbosely.
  --stream                     Stream the Docs agent's response.
  --force                      Re-download all documentation, not just version updates.
"""

from docopt import docopt
from docs_agent.helpers.log import logger


def main(version):
    args = docopt(__doc__, version=version) # type: ignore
    logger.debug(
        "Received CLI command with args: %s", {k: v for k, v in args.items() if v}
    )
    match args:
        case {
            "init": True,
            "<dir>": dir,
            "--non-interactive": non_interactive,
            "--silent": silent,
        }:
            from docs_agent.setup import main as setup

            setup(directory=dir or ".", non_interactive=non_interactive, silent=silent)
        case {
            "add": True,
            "<tool>": tools,
            "<version>": versions,
            "--non-interactive": noninteractive,
            "--silent": silent,
        }:
            from docs_agent.add_element import main as add_element

            add_element(
                tools=tools,
                versions=versions,
                noninteractive=noninteractive,
                silent=silent,
            )
        case {"config": True, "<option>": option, "<value>": value}:
            from docs_agent.config import get_or_set_option as configure

            configure(option=option, value=value)
        case {"ask": True, "<prompt>": prompt, "--stream": stream}:
            from docs_agent.agent import ask as ask

            ask(prompt=prompt, stream=stream)
        case {"chat": True}:
            from docs_agent.agent import chat as chat

            chat()
        case {"pull": True, "--force": force, "--silent": silent, "--verbose": verbose}:
            from docs_agent.update import main as update

            update(force=force, silent=silent, verbose=verbose)
        case {"update": True, "--force": force, "--silent": silent, "--verbose": verbose}:
            from docs_agent.update import main as update
            update(force=force, silent=silent, verbose=verbose)
        case _:
            logger.error("Given command is either invalid or not yet implemented.")
            logger.debug("Debug info: %s", args)
