from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def get_db_script_path() -> Path:
    return Path(__file__).parent / "../infra/db/scheme.sql"
