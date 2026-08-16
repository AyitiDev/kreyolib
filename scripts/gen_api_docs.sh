#!/usr/bin/env bash
# Generate API_REFERENCES.md using pydoc-markdown.
# Auto-discovers all kreyolib modules, skipping private/irrelevant stubs.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")"/.. && pwd)"
cd "$REPO_DIR"

MODULES=$(find src/kreyolib -name '*.py' \
    | sort \
    | sed \
        -e 's|^src/||' \
        -e 's|/|.|g' \
        -e 's|\.py$||' \
        -e 's|\.__init__$||'
)

ARGS=()
for mod in $MODULES; do
    ARGS+=(-m "$mod")
done

export PYTHONPATH="$REPO_DIR/src"
OUT="$REPO_DIR/API_REFERENCES.md"
pydoc-markdown "${ARGS[@]}" --render-toc > "$OUT"
LINES=$(wc -l < "$OUT")
echo "Done. Wrote $OUT ($LINES lines) / Fini. Ekri nan $OUT ($LINES liy)"