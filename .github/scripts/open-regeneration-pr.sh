#!/usr/bin/env bash
# Publish validated spec/client changes from a clean checkout of main.
set -euo pipefail

: "${GH_REPO:?GH_REPO must identify the SDK repository}"
branch="sdk/regenerate"
title="feat: regenerate SDK from upstream OpenAPI spec"

pr_number=$(gh pr list --repo "$GH_REPO" --base main --head "$branch" \
  --state open --json number,isCrossRepository \
  --jq 'map(select(.isCrossRepository == false))[0].number // empty')

git add -- api/openapi.yaml phenostore/gen/
if [[ "${INCLUDE_WRAPPER_CHANGES:-false}" == "true" ]]; then
  # The workflow enables this only after Claude adaptation and validation pass.
  git add -- phenostore/ examples/ tests/ README.md
fi
if git diff --cached --quiet; then
  echo "SDK and spec already match main."
  if [[ -n "$pr_number" ]]; then
    gh pr close "$pr_number" --repo "$GH_REPO"
  fi
  exit 0
fi

# An empty expected SHA requires a new branch; an existing SHA guards against
# overwriting a concurrent push. Only this automation's branch is replaced.
remote_sha=$(git ls-remote origin "refs/heads/$branch" | cut -f1)
git switch -C "$branch"
git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git commit -m "$title"
git push --force-with-lease="refs/heads/$branch:$remote_sha" \
  origin "HEAD:refs/heads/$branch"

body_file=$(mktemp)
trap 'rm -f "$body_file"' EXIT
cat > "$body_file" <<EOF
Regenerates the Python SDK from the upstream Phenostore API contract.

Spec identifier: ${SPEC_SHA:-manual regeneration from the committed spec}
Phenostore commit: ${PHENOSTORE_SHA:-not supplied}

Validation: tests, lint, type checking, generation consistency, and package build.
Any required automatic wrapper adaptations are included in this PR and have passed validation.
EOF

if [[ -n "$pr_number" ]]; then
  gh pr edit "$pr_number" --repo "$GH_REPO" --title "$title" --body-file "$body_file"
else
  gh pr create --repo "$GH_REPO" --base main --head "$branch" \
    --title "$title" --body-file "$body_file"
fi
