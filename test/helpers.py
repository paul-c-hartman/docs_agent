import chromadb
from chromadb import Settings
import os
import functools


@functools.cache
def init_chromadb_client():
    """Initialize and return a ChromaDB client."""
    chromadb_dir = os.path.join(".docs", "chromadb")
    if not os.path.exists(chromadb_dir):
        os.makedirs(chromadb_dir)
    client = chromadb.Client(
        Settings(chroma_db_impl="duckdb+parquet", persist_directory=chromadb_dir)
    )
    return client
