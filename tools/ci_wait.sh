#!/usr/bin/env bash
# Wait for the GitHub Actions run(s) on a commit and print the result.
#   bash tools/ci_wait.sh [sha] [max_seconds]
# Uses the FULL sha (no short-hash prefix matching) and filters by head_sha on the
# server. Always prints a final line: every run's conclusion, or TIMEOUT / NO RUN
# with the last state seen -- silence never means success. Exit 0 only if every
# run on the commit completed with conclusion=success.
sha=$(git rev-parse "${1:-HEAD}") || exit 2
max=${2:-1200}
repo=cylicamp/cylicamp
deadline=$((SECONDS + max)); last="none seen"
while [ $SECONDS -lt $deadline ]; do
  r=$(gh api "repos/$repo/actions/runs?head_sha=$sha&per_page=20" \
        --jq '.workflow_runs[] | "\(.name) #\(.run_number) \(.status) \(.conclusion)"' 2>/dev/null)
  if [ -n "$r" ]; then
    last=$r
    if ! grep -qv ' completed ' <<<"$r"; then
      echo "$r"
      grep -qv ' completed success$' <<<"$r" && { echo "FAILED: $sha"; exit 1; }
      echo "PASSED: $sha"; exit 0
    fi
  fi
  sleep 15
done
echo "TIMEOUT after ${max}s for $sha; last state: $last"
exit 3
