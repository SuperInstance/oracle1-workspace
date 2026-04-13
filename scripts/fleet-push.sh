#!/bin/bash
# Fleet Push — commit and push all active repos
# Run after any work session to keep GitHub current

source ~/.bashrc
export GITHUB_TOKEN=$(grep GITHUB_TOKEN ~/.bashrc | head -1 | sed 's/.*=//' | tr -d "'" | tr -d '"')

REPOS=(
  "/home/ubuntu/.openclaw/workspace:oracle1-workspace"
  "/tmp/holodeck-rust:holodeck-rust"
  "/tmp/openmanus-vessel:openmanus-vessel"
)

for ENTRY in "${REPOS[@]}"; do
  DIR="${ENTRY%%:*}"
  NAME="${ENTRY##*:}"
  
  if [ ! -d "$DIR/.git" ]; then
    continue
  fi
  
  cd "$DIR"
  
  if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    git add -A
    MSG="auto-push: $(date +%Y-%m-%d_%H%M)"
    git commit -m "$MSG" 2>/dev/null
  fi
  
  git pull --rebase 2>/dev/null
  PUSHED=$(git push 2>&1)
  
  if echo "$PUSHED" | grep -q "new commits\|up to date\|Everything"; then
    echo "✅ $NAME pushed"
  else
    echo "⚠️ $NAME: $PUSHED" | head -1
  fi
done
