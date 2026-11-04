"""Exercise the maintenance target's version selection and validation gate."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def maintenance(tmp_path):
    shutil.copyfile(ROOT / "Makefile", tmp_path / "Makefile")
    calls = tmp_path / "uv-calls.jsonl"
    uv = tmp_path / "uv"
    uv.write_text(
        f"#!{sys.executable}\n"
        + """
import json
import os
import sys
from pathlib import Path
args = sys.argv[1:]
with Path(os.environ["TEST_UV_CALLS"]).open("a") as stream:
    stream.write(json.dumps(args) + "\\n")
if args == ["run", "--locked", "pytest"] and os.environ.get("TEST_INCOMPATIBLE"):
    print("SDK contract tests failed", file=sys.stderr)
    raise SystemExit(1)
"""
    )
    uv.chmod(0o755)

    def run(*args, **settings):
        # This test also runs inside `make update-generator`; isolate its nested
        # make invocation from the caller's version and command-line overrides.
        env = dict(os.environ)
        for name in ["GENERATOR_VERSION", "MAKEFLAGS", "MFLAGS", "MAKELEVEL", "MAKEOVERRIDES"]:
            env.pop(name, None)
        result = subprocess.run(
            ["make", "update-generator", f"UV={uv}", *args],
            cwd=tmp_path,
            env={**env, "TEST_UV_CALLS": str(calls), **settings},
            capture_output=True,
            text=True,
        )
        return result, [json.loads(line) for line in calls.read_text().splitlines()]

    return run


@pytest.mark.parametrize("version", [None, "latest", "0.29.1"])
def test_version_selection_and_full_validation(maintenance, version):
    result, calls = maintenance(*([f"GENERATOR_VERSION={version}"] if version else []))
    assert result.returncode == 0, result.stderr
    requested = "openapi-python-client==0.29.1" if version == "0.29.1" else "openapi-python-client"
    assert calls[:2] == [
        ["remove", "--project", "tools", "--frozen", "openapi-python-client", "ruff"],
        ["add", "--project", "tools", "--bounds", "exact", "--upgrade", requested, "ruff"],
    ]
    assert calls[2:] == [
        ["run", "--project", "tools", "--locked", "python", "tools/generate.py"],
        ["run", "--locked", "pytest"],
        ["run", "--locked", "ruff", "check", "."],
        ["run", "--locked", "ruff", "format", "--check", "."],
        ["run", "--locked", "mypy"],
        ["run", "--project", "tools", "--locked", "python", "tools/generate.py", "--check"],
        ["build"],
    ]


def test_targeted_generator_contract_failure_stops_maintenance(maintenance):
    result, calls = maintenance("GENERATOR_VERSION=0.28.3", TEST_INCOMPATIBLE="1")
    assert result.returncode != 0
    assert "SDK contract tests failed" in result.stderr
    assert "openapi-python-client==0.28.3" in calls[1]
    assert calls[-1] == ["run", "--locked", "pytest"]
