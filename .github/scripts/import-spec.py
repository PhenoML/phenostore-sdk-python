"""Import a dispatch payload, keeping the committed spec intact on decode errors."""

import base64
import binascii
import gzip
import os
import re
import zlib
from pathlib import Path

if not re.fullmatch(r"[a-fA-F0-9]{7,64}", os.environ.get("SPEC_SHA", "")):
    raise SystemExit("spec_sha must be a hexadecimal commit or content identifier")

encoding = os.environ.get("SPEC_ENCODING") or "base64"
if encoding not in ("base64", "gzip+base64"):
    raise SystemExit("spec_encoding must be base64 or gzip+base64")
try:
    spec = base64.b64decode(os.environ.get("SPEC_B64", ""), validate=True)
except (binascii.Error, ValueError):
    raise SystemExit("spec_b64 must be a valid base64 OpenAPI document") from None
if encoding == "gzip+base64":
    try:
        spec = gzip.decompress(spec)
    except (gzip.BadGzipFile, EOFError, zlib.error):
        raise SystemExit("spec_b64 must contain a valid gzip OpenAPI document") from None
if not spec:
    raise SystemExit("spec_b64 must contain the upstream OpenAPI document")
Path("api/openapi.yaml").write_bytes(spec)
