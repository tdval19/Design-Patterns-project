from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def get_db_script_path() -> Path:
    return Path(__file__).parent / "../infra/db/scheme.sql"
