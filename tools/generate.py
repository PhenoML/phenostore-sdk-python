"""Generate into a temporary directory; check mode never changes committed files."""

from __future__ import annotations

import argparse
import difflib
import shutil
import subprocess
import tempfile
from pathlib import Path

from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as temp:
        work = Path(temp)
        yaml = YAML()
        spec = yaml.load((ROOT / "api/openapi.yaml").read_text())
        # 0.29.1 emits an optional body (and sometimes an undefined Unset) for
        # equivalent bodies with multiple media types. Keep the first encoding
        # of each schema in the generator input, preferring application/fhir+json
        # as listed upstream. The imported spec is never modified.
        for path in spec["paths"].values():
            for operation in path.values():
                if not isinstance(operation, dict) or "requestBody" not in operation:
                    continue
                content = operation["requestBody"].get("content", {})
                seen = []
                for media_type, body in list(content.items()):
                    if body in seen:
                        del content[media_type]
                    else:
                        seen.append(body)
        source = work / "openapi.yaml"
        with source.open("w") as stream:
            yaml.dump(spec, stream)
        output = work / "gen"
        subprocess.run(
            [
                "openapi-python-client",
                "generate",
                "--path",
                str(source),
                "--config",
                str(ROOT / "openapi-python-client.yaml"),
                "--meta",
                "none",
                "--output-path",
                str(output),
            ],
            check=True,
        )
        # Isolate formatting from repository settings and machine-local config.
        subprocess.run(
            ["ruff", "check", "--isolated", "--fix-only", "--select", "F,I", str(output)],
            check=True,
        )
        subprocess.run(["ruff", "format", "--isolated", str(output)], check=True)
        generated = {
            p.relative_to(output): p.read_bytes()
            for p in output.rglob("*")
            if p.is_file() and ".ruff_cache" not in p.parts
        }
        destination = ROOT / "phenostore/gen"
        if args.check:
            committed = {
                p.relative_to(destination): p.read_bytes()
                for p in destination.rglob("*")
                if p.is_file() and "__pycache__" not in p.parts
            }
            if generated != committed:
                for name in sorted(generated.keys() | committed.keys()):
                    before, after = committed.get(name, b""), generated.get(name, b"")
                    if before != after:
                        print(
                            "".join(
                                difflib.unified_diff(
                                    before.decode().splitlines(True),
                                    after.decode().splitlines(True),
                                    fromfile=f"committed/{name}",
                                    tofile=f"generated/{name}",
                                )
                            )
                        )
                raise SystemExit("Generated files are stale. Run 'make generate'.")
        else:
            if destination.exists():
                shutil.rmtree(destination)
            destination.mkdir(parents=True)
            for name, data in generated.items():
                target = destination / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)


if __name__ == "__main__":
    main()
