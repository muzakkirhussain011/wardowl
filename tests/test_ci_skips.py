"""tests/conftest.py fails a run that skips anything unexpected when WARDOWL_CI_NO_SKIPS=1, as CI's
test job sets it, and changes nothing without it."""

from __future__ import annotations

from pathlib import Path

import pytest

pytest_plugins = ["pytester"]

CONFTEST = (Path(__file__).resolve().parent / "conftest.py").read_text(encoding="utf-8")


@pytest.fixture
def run(pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch):
    pytester.makeconftest(CONFTEST)
    pytester.makepyfile(test_other="def test_it():\n    pass\n")  # so that every run collects a test

    def run(source: str, flag: str | None) -> pytest.RunResult:
        if flag is None:
            monkeypatch.delenv("WARDOWL_CI_NO_SKIPS", raising=False)
        else:
            monkeypatch.setenv("WARDOWL_CI_NO_SKIPS", flag)
        pytester.makepyfile(test_suite=source)
        return pytester.runpytest("-p", "no:cacheprovider")

    return run


SKIPPED_TEST = "import pytest\n\ndef test_it():\n    pytest.skip('set WARDOWL_TEST_EXAMPLE_URL to run')\n"
SKIPPED_MODULE = "import pytest\n\npytest.importorskip('a_module_that_is_not_installed')\n\ndef test_it():\n    pass\n"
PINECONE = "import pytest\n\ndef test_it():\n    pytest.skip('set WARDOWL_TEST_PINECONE_API_KEY to run')\n"
XFAIL = "import pytest\n\n@pytest.mark.xfail(strict=True)\ndef test_it():\n    assert False\n"


@pytest.mark.parametrize("source", [SKIPPED_TEST, SKIPPED_MODULE])
def test_an_unexpected_skip_fails_the_run(run, source):
    result = run(source, "1")
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    result.stdout.fnmatch_lines(["*WARDOWL_CI_NO_SKIPS=1, but 1 skipped:*", "*test_suite*"])


@pytest.mark.parametrize("source", [SKIPPED_TEST, SKIPPED_MODULE])
def test_without_the_variable_a_skip_passes(run, source):
    assert run(source, None).ret == pytest.ExitCode.OK
    assert run(source, "0").ret == pytest.ExitCode.OK


@pytest.mark.parametrize("source", [PINECONE, XFAIL])
def test_the_pinecone_service_tests_and_expected_failures_pass(run, source):
    assert run(source, "1").ret == pytest.ExitCode.OK
