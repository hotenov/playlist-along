"""Integration test fixtures."""
from _pytest.config import Config


def pytest_configure(config: Config) -> None:
    """Pytest configuration hook."""
    config.addinivalue_line(
        "markers",
        "datafiles: load prepared datafiles",
    )
