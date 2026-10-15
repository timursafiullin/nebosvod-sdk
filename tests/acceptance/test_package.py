"""Acceptance tests for the SDK package skeleton."""

import re
import subprocess
import sys
import zipfile
from email.parser import Parser
from importlib.metadata import version
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
EXPECTED_VERSION = "0.1.0.dev0"
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "ci.yml"
# Files that legitimately name what must never be added to this public repository.
HYGIENE_EXEMPT = {"AGENTS.md", "CLAUDE.md", "tests/acceptance/test_package.py"}
PRIVATE_MARKERS = re.compile(r"\.agents/|ADR-\d{4}|nebosvod-legacy|claude\.ai|pi-bridge|\bT-\d{4}\b")


def test_package_imports_and_reports_its_version() -> None:
    """The distribution installs and its version is single-sourced."""
    import nebosvod_sdk

    assert nebosvod_sdk.__version__ == version("nebosvod-sdk") == EXPECTED_VERSION


@pytest.fixture(scope="module")
def wheel(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Build the wheel once with uv."""
    output = tmp_path_factory.mktemp("dist")
    result = subprocess.run(
        ["uv", "build", "--wheel", "--out-dir", str(output)],
        capture_output=True,
        text=True,
        check=False,
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    (built,) = output.glob("nebosvod_sdk-*.whl")
    return built


def test_wheel_is_typed_licensed_and_dependency_free(wheel: Path) -> None:
    """The wheel ships py.typed, the Apache-2.0 license and notice, and no runtime dependencies."""
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        metadata_name = next(name for name in names if name.endswith(".dist-info/METADATA"))
        metadata = Parser().parsestr(archive.read(metadata_name).decode("utf-8"))

    assert "nebosvod_sdk/__init__.py" in names
    assert "nebosvod_sdk/py.typed" in names
    assert any(name.endswith("/licenses/LICENSE") for name in names)
    assert any(name.endswith("/licenses/NOTICE") for name in names)
    assert metadata["Name"] == "nebosvod-sdk"
    assert metadata["Version"] == EXPECTED_VERSION
    assert metadata["License-Expression"] == "Apache-2.0"
    assert metadata["Requires-Python"] == ">=3.12"
    assert metadata.get_all("Requires-Dist") is None


def test_wheel_installs_into_a_clean_environment(wheel: Path, tmp_path: Path) -> None:
    """A user can install the wheel without this checkout and import it."""
    venv = tmp_path / "venv"
    subprocess.run(["uv", "venv", "--python", sys.executable, str(venv)], check=True, capture_output=True)
    python = venv / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    subprocess.run(
        ["uv", "pip", "install", "--python", str(python), str(wheel)], check=True, capture_output=True
    )
    result = subprocess.run(
        [str(python), "-c", "import nebosvod_sdk; print(nebosvod_sdk.__version__)"],
        capture_output=True,
        text=True,
        check=False,
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == EXPECTED_VERSION


def test_repository_contains_no_private_references() -> None:
    """Public repository hygiene: no internal paths, decision ids, task ids or session links."""
    tracked = subprocess.run(
        ["git", "ls-files"], capture_output=True, text=True, check=True, cwd=REPO_ROOT
    ).stdout.splitlines()
    offenders = []
    for relative in tracked:
        if relative in HYGIENE_EXEMPT or relative.endswith(".lock"):
            continue
        text = (REPO_ROOT / relative).read_text(encoding="utf-8", errors="replace")
        offenders += [f"{relative}: {match.group(0)}" for match in PRIVATE_MARKERS.finditer(text)]
    assert offenders == []


def test_ci_runs_checks_on_linux_and_windows() -> None:
    """CI runs the full check list on Linux and Windows."""
    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    (job,) = workflow["jobs"].values()
    matrix = job["strategy"]["matrix"]
    assert {"ubuntu", "windows"} <= {os_name.split("-")[0] for os_name in matrix["os"]}
    commands = "\n".join(step.get("run", "") for step in job["steps"])
    for command in [
        "uv sync --locked",
        "uv run ruff format --check .",
        "uv run ruff check .",
        "uv run mypy",
        "uv run pytest",
    ]:
        assert command in commands, command
