"""Unit tests for package version metadata."""

from importlib.metadata import version

import nebosvod_sdk


def test_version_matches_distribution_metadata() -> None:
    """Expose the installed distribution version as a non-empty string."""
    assert isinstance(nebosvod_sdk.__version__, str)
    assert nebosvod_sdk.__version__
    assert nebosvod_sdk.__version__ == version("nebosvod-sdk")
