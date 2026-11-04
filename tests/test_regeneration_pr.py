"""Run the publishing script against a local Git remote and a fake GitHub CLI."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / ".github/scripts/open-regeneration-pr.sh"


def git(directory, *args):
    return subprocess.run(
        ["git", "-C", str(directory), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


@pytest.fixture
def publishing(tmp_path):
    remote, checkout = tmp_path / "remote.git", tmp_path / "checkout"
    subprocess.run(
        ["git", "init", "--bare", "--initial-branch=main", str(remote)],
        check=True,
        capture_output=True,
    )
    subprocess.run(["git", "clone", str(remote), str(checkout)], check=True, capture_output=True)
    git(checkout, "config", "user.name", "Test")
    git(checkout, "config", "user.email", "test@example.test")
    for name in [
        "api/openapi.yaml",
        "phenostore/gen/client.py",
        "phenostore/client.py",
        "tests/test_client.py",
        "examples/basic.py",
        "README.md",
        ".github/workflows/ci.yml",
    ]:
        target = checkout / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("original\n")
    git(checkout, "add", ".")
    git(checkout, "commit", "-m", "initial")
    git(checkout, "push", "origin", "main")

    fake_bin, calls = tmp_path / "bin", tmp_path / "gh-calls.jsonl"
    fake_bin.mkdir()
    fake_gh = fake_bin / "gh"
    fake_gh.write_text(
        f"#!{sys.executable}\n"
        + """
import json
import os
import sys
from pathlib import Path
args = sys.argv[1:]
entry = {"args": args}
if "--body-file" in args:
    entry["body"] = Path(args[args.index("--body-file") + 1]).read_text()
with Path(os.environ["TEST_GH_CALLS"]).open("a") as stream:
    stream.write(json.dumps(entry) + "\\n")
if args[:2] == ["pr", os.environ.get("TEST_GH_FAIL", "")]:
    raise SystemExit(1)
if args[:2] == ["pr", "list"]:
    print(os.environ.get("TEST_PR_NUMBER", ""))
"""
    )
    fake_gh.chmod(0o755)
    env = {
        **os.environ,
        "PATH": f"{fake_bin}:{os.environ['PATH']}",
        "GH_REPO": "example/sdk",
        "GH_TOKEN": "fake-test-token",
        "SPEC_SHA": "deadbeef",
        "PHENOSTORE_SHA": "deadbeef01234567",
        "TEST_GH_CALLS": str(calls),
    }

    class Publishing:
        def run(self, *args, **settings):
            return subprocess.run(
                ["bash", str(SCRIPT), *args],
                cwd=checkout,
                env={**env, **settings},
                capture_output=True,
                text=True,
            )

        def change(self):
            (checkout / "api/openapi.yaml").write_text("updated spec\n")
            (checkout / "phenostore/gen/client.py").write_text("updated client\n")
            (checkout / "README.md").write_text("unrelated change\n")

        def calls(self):
            return [json.loads(line) for line in calls.read_text().splitlines()]

        def remote_branch(self):
            return git(remote, "rev-parse", "--verify", "refs/heads/sdk/regenerate")

        def check(self, **settings):
            output = tmp_path / "github-output"
            output.write_text("")
            result = self.run("--check", GITHUB_OUTPUT=str(output), **settings)
            assert result.returncode == 0, result.stderr
            return dict(line.split("=", 1) for line in output.read_text().splitlines())

    context = Publishing()
    context.checkout, context.remote = checkout, remote
    return context


def test_no_changes_does_not_push_or_open_a_pr(publishing):
    result = publishing.run()
    assert result.returncode == 0, result.stderr
    assert "already match main" in result.stdout
    assert [entry["args"][1] for entry in publishing.calls()] == ["list"]
    assert git(publishing.remote, "branch", "--list", "sdk/regenerate") == ""


def test_no_changes_closes_an_obsolete_pr(publishing):
    result = publishing.run(TEST_PR_NUMBER="42")
    assert result.returncode == 0, result.stderr
    assert publishing.calls()[-1]["args"] == ["pr", "close", "42", "--repo", "example/sdk"]
    assert git(publishing.remote, "branch", "--list", "sdk/regenerate") == ""


def test_create_pr_commits_only_generated_changes(publishing):
    original_main = git(publishing.remote, "rev-parse", "main")
    publishing.change()
    result = publishing.run()
    assert result.returncode == 0, result.stderr
    assert git(publishing.remote, "rev-parse", "main") == original_main
    assert git(publishing.remote, "show", "sdk/regenerate:api/openapi.yaml") == "updated spec"
    assert (
        git(publishing.remote, "show", "sdk/regenerate:phenostore/gen/client.py")
        == "updated client"
    )
    assert git(publishing.remote, "show", "sdk/regenerate:README.md") == "original"
    request = publishing.calls()[-1]
    assert request["args"][:2] == ["pr", "create"]
    assert request["args"][request["args"].index("--head") + 1] == "sdk/regenerate"
    assert "deadbeef" in request["body"] and "deadbeef01234567" in request["body"]


def test_update_existing_pr_and_manual_metadata(publishing):
    publishing.change()
    assert publishing.run().returncode == 0
    git(publishing.checkout, "switch", "main")
    (publishing.checkout / "api/openapi.yaml").write_text("newer spec\n")
    (publishing.checkout / ".commit-message").write_text("fix: correct response parsing\n")
    result = publishing.run(TEST_PR_NUMBER="42", SPEC_SHA="", PHENOSTORE_SHA="")
    assert result.returncode == 0, result.stderr
    assert git(publishing.remote, "show", "sdk/regenerate:api/openapi.yaml") == "newer spec"
    assert sum(entry["args"][:2] == ["pr", "create"] for entry in publishing.calls()) == 1
    request = publishing.calls()[-1]
    assert request["args"][:3] == ["pr", "edit", "42"]
    assert "manual regeneration" in request["body"]
    assert request["args"][request["args"].index("--title") + 1] == (
        "fix: correct response parsing"
    )
    assert git(publishing.remote, "log", "-1", "--format=%s", "sdk/regenerate") == (
        "fix: correct response parsing"
    )


def test_validated_wrapper_adaptations_are_committed(publishing):
    publishing.change()
    for name in ["phenostore/client.py", "tests/test_client.py", "examples/basic.py", "README.md"]:
        (publishing.checkout / name).write_text("adapted\n")
    (publishing.checkout / "tests/test_new_contract.py").write_text("new regression coverage\n")
    (publishing.checkout / ".github/workflows/ci.yml").write_text("unrelated workflow change\n")

    result = publishing.run(INCLUDE_WRAPPER_CHANGES="true")
    assert result.returncode == 0, result.stderr
    for name in ["phenostore/client.py", "tests/test_client.py", "examples/basic.py", "README.md"]:
        assert git(publishing.remote, "show", f"sdk/regenerate:{name}") == "adapted"
    assert git(publishing.remote, "show", "sdk/regenerate:tests/test_new_contract.py") == (
        "new regression coverage"
    )
    assert git(publishing.remote, "show", "sdk/regenerate:.github/workflows/ci.yml") == "original"


def test_wrapper_adaptations_require_explicit_inclusion(publishing):
    publishing.change()
    (publishing.checkout / "phenostore/client.py").write_text("unvalidated adaptation\n")
    result = publishing.run(INCLUDE_WRAPPER_CHANGES="false")
    assert result.returncode == 0, result.stderr
    assert git(publishing.remote, "show", "sdk/regenerate:phenostore/client.py") == "original"


def test_lookup_failure_does_not_push(publishing):
    publishing.change()
    result = publishing.run(TEST_GH_FAIL="list")
    assert result.returncode != 0
    assert git(publishing.remote, "branch", "--list", "sdk/regenerate") == ""


def test_pr_creation_failure_is_reported_and_can_be_retried(publishing):
    publishing.change()
    assert publishing.run(TEST_GH_FAIL="create").returncode != 0
    publishing.remote_branch()  # The push succeeded before the API failure.
    git(publishing.checkout, "switch", "main")
    publishing.change()
    result = publishing.run()
    assert result.returncode == 0, result.stderr
    assert publishing.calls()[-1]["args"][:2] == ["pr", "create"]


def test_concurrent_branch_update_is_not_overwritten(publishing):
    publishing.change()
    assert publishing.run().returncode == 0
    previous = publishing.remote_branch()
    (publishing.checkout / "api/openapi.yaml").write_text("concurrent edit\n")
    git(publishing.checkout, "add", "api/openapi.yaml")
    git(publishing.checkout, "commit", "-m", "concurrent change")
    concurrent = git(publishing.checkout, "rev-parse", "HEAD")
    git(publishing.checkout, "push", "origin", "sdk/regenerate")
    git(publishing.remote, "update-ref", "refs/heads/sdk/regenerate", previous)
    git(publishing.checkout, "switch", "main")
    publishing.change()
    # Advance the remote after the script reads its lease, during git commit.
    hook = publishing.checkout / ".git/hooks/pre-commit"
    hook.write_text(
        '#!/bin/sh\nexec git --git-dir="$TEST_REMOTE" update-ref '
        'refs/heads/sdk/regenerate "$TEST_CONCURRENT_SHA"\n'
    )
    hook.chmod(0o755)
    result = publishing.run(
        TEST_PR_NUMBER="42", TEST_REMOTE=str(publishing.remote), TEST_CONCURRENT_SHA=concurrent
    )
    assert result.returncode != 0
    assert publishing.remote_branch() == concurrent
    assert publishing.calls()[-1]["args"][:2] == ["pr", "list"]


@pytest.mark.parametrize(
    "title",
    [
        "feat: add Encounter support",
        "feat!: remove obsolete resource exports",
        "fix: preserve empty Bundle responses",
        "chore: refresh generated documentation",
    ],
)
def test_classified_title_is_used_for_commit_and_pr(publishing, title):
    publishing.change()
    selected = publishing.check()
    assert selected["changed"] == "true"
    (publishing.checkout / ".commit-message").write_text(title + "\n")
    result = publishing.run(VALIDATED_TREE=selected["tree"])
    assert result.returncode == 0, result.stderr
    assert git(publishing.remote, "log", "-1", "--format=%s", "sdk/regenerate") == title
    request = publishing.calls()[-1]
    assert request["args"][request["args"].index("--title") + 1] == title
    assert "Review the title before merging" in request["body"]
    assert not (publishing.checkout / ".commit-message").exists()
    assert ".commit-message" not in git(
        publishing.remote, "ls-tree", "--name-only", "sdk/regenerate"
    )


@pytest.mark.parametrize(
    "message",
    [
        None,
        "",
        "\n",
        "feat:",
        "fix:  two spaces",
        "fix!: unsupported breaking prefix",
        "chore!: unsupported breaking prefix",
        "docs: unsupported prefix",
        "feat: " + "x" * 67,
        "fix: first line\nchore: second line",
        "fix: control\rcharacter",
    ],
)
def test_missing_or_invalid_classification_uses_fixed_fallback(publishing, message):
    publishing.change()
    if message is not None:
        (publishing.checkout / ".commit-message").write_text(message)
    result = publishing.run()
    assert result.returncode == 0, result.stderr
    fallback = "feat: regenerate SDK from upstream OpenAPI spec"
    assert git(publishing.remote, "log", "-1", "--format=%s", "sdk/regenerate") == fallback
    request = publishing.calls()[-1]
    assert request["args"][request["args"].index("--title") + 1] == fallback
    assert not (publishing.checkout / ".commit-message").exists()


def test_failed_classifier_discards_partial_output(publishing):
    publishing.change()
    (publishing.checkout / ".commit-message").write_text("chore: incomplete classification\n")
    result = publishing.run(CLASSIFICATION_SUCCEEDED="false")
    assert result.returncode == 0, result.stderr
    assert git(publishing.remote, "log", "-1", "--format=%s", "sdk/regenerate") == (
        "feat: regenerate SDK from upstream OpenAPI spec"
    )
    assert not (publishing.checkout / ".commit-message").exists()


@pytest.mark.parametrize("existing_pr", ["", "42"])
def test_message_only_is_a_noop(publishing, existing_pr):
    message = publishing.checkout / ".commit-message"
    message.write_text("feat: this must not create a PR\n")
    git(publishing.checkout, "add", ".commit-message")
    result = publishing.run(TEST_PR_NUMBER=existing_pr)
    assert result.returncode == 0, result.stderr
    assert "already match main" in result.stdout
    assert not message.exists()
    assert [entry["args"][1] for entry in publishing.calls()] == (
        ["list", "close"] if existing_pr else ["list"]
    )
    assert git(publishing.remote, "branch", "--list", "sdk/regenerate") == ""


def test_check_noop_clears_stale_message_without_contacting_github(publishing):
    message = publishing.checkout / ".commit-message"
    message.write_text("feat: stale classification\n")
    selected = publishing.check()
    assert selected == {
        "tree": git(publishing.checkout, "rev-parse", "HEAD^{tree}"),
        "changed": "false",
    }
    assert not message.exists()


@pytest.mark.parametrize(
    ("path", "include_wrapper"),
    [
        ("api/openapi.yaml", "false"),
        ("phenostore/gen/client.py", "false"),
        ("phenostore/client.py", "true"),
        ("tests/test_new_contract.py", "true"),
    ],
)
def test_classifier_cannot_change_validated_files(publishing, path, include_wrapper):
    publishing.change()
    selected = publishing.check(INCLUDE_WRAPPER_CHANGES=include_wrapper)
    (publishing.checkout / path).write_text("unvalidated classifier edit\n")
    message = publishing.checkout / ".commit-message"
    message.write_text("fix: plausible title\n")
    result = publishing.run(
        VALIDATED_TREE=selected["tree"], INCLUDE_WRAPPER_CHANGES=include_wrapper
    )
    assert result.returncode != 0
    assert "differ from the validated diff" in result.stderr
    assert not message.exists()
    assert git(publishing.remote, "branch", "--list", "sdk/regenerate") == ""


def test_classifier_cannot_delete_validated_files(publishing):
    publishing.change()
    selected = publishing.check()
    (publishing.checkout / "phenostore/gen/client.py").unlink()
    result = publishing.run(VALIDATED_TREE=selected["tree"])
    assert result.returncode != 0
    assert "differ from the validated diff" in result.stderr
    assert git(publishing.remote, "branch", "--list", "sdk/regenerate") == ""


def test_pre_staged_unselected_changes_are_excluded(publishing):
    publishing.change()
    git(publishing.checkout, "add", "README.md")
    selected = publishing.check()
    (publishing.checkout / ".github/workflows/ci.yml").write_text("unvalidated workflow\n")
    git(publishing.checkout, "add", ".github/workflows/ci.yml")
    result = publishing.run(VALIDATED_TREE=selected["tree"])
    assert result.returncode == 0, result.stderr
    assert git(publishing.remote, "show", "sdk/regenerate:README.md") == "original"
    assert git(publishing.remote, "show", "sdk/regenerate:.github/workflows/ci.yml") == "original"
