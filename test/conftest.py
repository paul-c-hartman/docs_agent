import pytest
import shutil
from pathlib import Path
from docs_agent.helpers.chromadb import DB

@pytest.fixture(scope="function")
def with_persistence():
    tmp_root = Path(".docs", "test")
    # Test setup
    db_dir = tmp_root / "chromadb"
    manifest = tmp_root / "elements.yaml"
    config = tmp_root / "config.yaml"
    db = DB(persist_directory=db_dir.as_posix())

    yield db, manifest, config

    # Test cleanup
    try:
        from chromadb.api.shared_system_client import SharedSystemClient
        SharedSystemClient.clear_system_cache()
    except Exception:
        pass
    shutil.rmtree(db_dir, ignore_errors=True)
    if manifest.exists():
        manifest.unlink()
    if config.exists():
        config.unlink()