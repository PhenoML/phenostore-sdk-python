"""Exercise legacy and compressed upstream spec imports without running generation."""

from __future__ import annotations

import base64
import gzip
import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / ".github/scripts/import-spec.py"
SPEC = b"openapi: 3.0.0\n"


@pytest.fixture
def importing(tmp_path):
    spec_file = tmp_path / "api/openapi.yaml"
    spec_file.parent.mkdir()
    spec_file.write_bytes(b"original\n")

    def run(payload, **settings):
        env = {key: value for key, value in os.environ.items() if not key.startswith("SPEC_")}
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=tmp_path,
            env={**env, "SPEC_SHA": "deadbeef", "SPEC_B64": payload, **settings},
            capture_output=True,
            text=True,
        )
        return result, spec_file.read_bytes()

    return run


@pytest.mark.parametrize("encoding", [None, "", "base64", "gzip+base64"])
def test_import_spec(importing, encoding):
    data = gzip.compress(SPEC) if encoding == "gzip+base64" else SPEC
    settings = {} if encoding is None else {"SPEC_ENCODING": encoding}
    result, spec = importing(base64.b64encode(data).decode(), **settings)
    assert result.returncode == 0, result.stderr
    assert spec == SPEC


@pytest.mark.parametrize(
    ("payload", "settings"),
    [
        ("", {}),
        ("invalid!", {}),
        (base64.b64encode(SPEC).decode(), {"SPEC_SHA": ""}),
        (base64.b64encode(SPEC).decode(), {"SPEC_SHA": "../../escape"}),
        (base64.b64encode(SPEC).decode(), {"SPEC_SHA": "a" * 65}),
        (base64.b64encode(SPEC).decode(), {"SPEC_ENCODING": "unknown"}),
        (base64.b64encode(SPEC).decode(), {"SPEC_ENCODING": "gzip+base64"}),
        (base64.b64encode(gzip.compress(b"")).decode(), {"SPEC_ENCODING": "gzip+base64"}),
        (base64.b64encode(gzip.compress(SPEC)[:-4]).decode(), {"SPEC_ENCODING": "gzip+base64"}),
    ],
)
def test_invalid_payload_preserves_committed_spec(importing, payload, settings):
    result, spec = importing(payload, **settings)
    assert result.returncode != 0
    assert spec == b"original\n"
