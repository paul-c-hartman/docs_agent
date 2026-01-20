"""CLI entry point."""

from docs_agent.cli import main as start_cli
from docs_agent import __version__

def main():
    start_cli(__version__)