"""The supported configurations page declares the same minimum versions as pyproject.toml."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "docs" / "support.md"


def _floors() -> dict[str, set[str]]:
    """Each package an extra names, with every minimum version the extras give it."""
    extras = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["optional-dependencies"]
    floors: dict[str, set[str]] = {}
    for requirement in (r for requirements in extras.values() for r in requirements):
        found = re.fullmatch(r"([A-Za-z0-9_.-]+)(?:\[[^\]]*\])?>=([0-9][0-9.]*)(?:;.*)?", requirement.strip())
        if found:
            floors.setdefault(found[1].lower(), set()).add(found[2])
    return floors


def test_every_declared_minimum_on_the_page_is_the_one_pyproject_declares():
    if not PAGE.exists():
        pytest.skip("docs/ is not in this tree (the source distribution leaves it out)")
    declared = re.findall(r"`([A-Za-z0-9_.-]+)>=([0-9][0-9.]*)`", PAGE.read_text(encoding="utf-8"))
    assert len(declared) >= 15, declared  # the version tables were found
    floors = _floors()
    for name, version in declared:
        assert name.lower() in floors, f"support.md declares {name}>={version}, which no extra names"
        given = floors[name.lower()]
        assert given == {version}, f"support.md declares {name}>={version}, pyproject.toml >={sorted(given)}"
