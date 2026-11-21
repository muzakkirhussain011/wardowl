"""Settings shared by every test module.

Each suite that needs a store, a permission service or an extra skips itself when it is missing,
so a run without them stays green. CI's test job installs every extra and starts every service, and
sets WARDOWL_CI_NO_SKIPS=1 so that a suite that skips there fails the run instead: without it, a
lost extra or a renamed WARDOWL_TEST_* variable would drop a whole suite silently.
"""

from __future__ import annotations

import os

import pytest

# Skips that the test job expects: only the separate `pinecone` job receives the Pinecone key.
EXPECTED_SKIPS = ("set WARDOWL_TEST_PINECONE_API_KEY",)


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    if os.environ.get("WARDOWL_CI_NO_SKIPS") != "1":
        return
    reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    if reporter is None:
        return
    skipped = [r for r in reporter.stats.get("skipped", []) if not any(e in str(r.longrepr) for e in EXPECTED_SKIPS)]
    if skipped:
        reporter.write_line(f"WARDOWL_CI_NO_SKIPS=1, but {len(skipped)} skipped:", red=True)
        for report in skipped:
            reporter.write_line(f"  {report.nodeid}: {report.longrepr}", red=True)
        session.exitstatus = pytest.ExitCode.TESTS_FAILED
