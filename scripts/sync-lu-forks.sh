#!/bin/bash
# =============================================================================
# sync-lu-forks.sh - Sync SuperInstance forks to Lucineer parent repos
# =============================================================================
# This script force-pushes the latest commit from each Lucineer parent to its
# corresponding SuperInstance fork, keeping them in sync.
#
# Usage: ./sync-lu-forks.sh [--dry-run]
#   --dry-run  Show what would be pushed without actually pushing
#
# Cron setup (daily at 3am):
#   sudo cp sync-lu-forks.sh /usr/local/bin/sync-lu-forks.sh
#   sudo chmod +x /usr/local/bin/sync-lu-forks.sh
#   (crontab -l 2>/dev/null; echo "0 3 * * * /usr/local/bin/sync-lu-forks.sh >> /var/log/sync-lu-forks.log 2>&1") | crontab -
#
# Or as systemd timer (see sync-lu-forks.timer & sync-lu-forks.service)
# =============================================================================

set -euo pipefail

TOKEN="${GITHUB_TOKEN:-}"
REPO_PAIRS=(
    "Lucineer/edge-llama:SuperInstance/edge-llama"
    "Lucineer/plato-tools:SuperInstance/plato-tools"
    "Lucineer/cocapn-architecture:SuperInstance/cocapn-architecture"
    "Lucineer/cocapn-chat:SuperInstance/cocapn-chat"
    "Lucineer/cocapn-go:SuperInstance/cocapn-go"
    "Lucineer/cocapn-py:SuperInstance/cocapn-py"
    "Lucineer/cocapn-sdk:SuperInstance/cocapn-sdk"
)

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
fi

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

get_sha() {
    local repo="$1"
    local sha
    sha=$(curl -sSf -H "Authorization: token ${TOKEN}" \
        "https://api.github.com/repos/${repo}/git/ref/heads/main" \
        | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['object']['sha'])" 2>/dev/null \
        || curl -sSf -H "Authorization: token ${TOKEN}" \
        "https://api.github.com/repos/${repo}/git/ref/heads/master" \
        | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['object']['sha'])" 2>/dev/null)
    echo "${sha}"
}

sync_repo() {
    local parent="$1"
    local fork="$2"
    local parent_sha fork_sha

    log "Checking ${parent} -> ${fork}"

    parent_sha=$(get_sha "${parent}")
    if [[ -z "${parent_sha}" ]]; then
        log "ERROR: Could not get SHA for ${parent}"
        return 1
    fi

    fork_sha=$(get_sha "${fork}")
    if [[ -z "${fork_sha}" ]]; then
        log "ERROR: Could not get SHA for ${fork}"
        return 1
    fi

    log "  Parent: ${parent_sha}"
    log "  Fork:   ${fork_sha}"

    if [[ "${parent_sha}" == "${fork_sha}" ]]; then
        log "  Already in sync, skipping"
        return 0
    fi

    if [[ "${DRY_RUN}" == "true" ]]; then
        log "  [DRY-RUN] Would force-push ${parent_sha} -> ${fork}"
        return 0
    fi

    # Clone fork, set parent as upstream, force-push
    local tmpdir
    tmpdir=$(mktemp -d)
    trap "rm -rf ${tmpdir}" EXIT

    git clone --bare "https://github.com/${fork}.git" "${tmpdir}" 2>/dev/null
    cd "${tmpdir}"
    git push "https://${TOKEN}@github.com/${fork}.git" "${parent_sha}:refs/heads/main" --force 2>/dev/null \
        || git push "https://${TOKEN}@github.com/${fork}.git" "${parent_sha}:refs/heads/master" --force 2>/dev/null

    log "  Force-pushed ${parent_sha} -> ${fork}"
}

# --- Main ---
if [[ -z "${TOKEN}" ]]; then
    log "ERROR: GITHUB_TOKEN env var not set"
    exit 1
fi

log "Starting Lucineer -> SuperInstance sync"
if [[ "${DRY_RUN}" == "true" ]]; then
    log "DRY-RUN mode enabled, no changes will be made"
fi

for pair in "${REPO_PAIRS[@]}"; do
    parent="${pair%%:*}"
    fork="${pair#*:}"
    sync_repo "${parent}" "${fork}" || log "Failed to sync ${fork}"
done

log "Sync complete"