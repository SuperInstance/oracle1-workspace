#!/usr/bin/env bash
# ============================================================
# git-agent installer — one-liner setup
# Usage: curl -fsSL https://raw.githubusercontent.com/SuperInstance/git-agent/main/install.sh | bash
#   Or:  bash install.sh [--vessel owner/repo] [--token ghpxxx]
# ============================================================
set -euo pipefail

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

VERSION="0.1.0"
INSTALL_DIR="${GIT_AGENT_HOME:-$HOME/.git-agent}"
BIN_DIR="$HOME/.local/bin"
REPO_URL="https://github.com/SuperInstance/git-agent"

info()  { echo -e "${CYAN}ℹ${NC} $*"; }
ok()    { echo -e "${GREEN}✓${NC} $*"; }
warn()  { echo -e "${YELLOW}⚠${NC} $*"; }
die()   { echo -e "${RED}✗${NC} $*"; exit 1; }

# ---- Parse args ----
VESSEL=""
TOKEN=""
SKIP_ONBOARD=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --vessel)   VESSEL="$2"; shift 2 ;;
    --token)    TOKEN="$2"; shift 2 ;;
    --skip)     SKIP_ONBOARD=true; shift ;;
    --help|-h)
      echo "Usage: bash install.sh [--vessel owner/repo] [--token ghp_xxx] [--skip]"
      echo ""
      echo "  --vessel   Vessel repo (owner/name) — the agent's identity"
      echo "  --token    GitHub personal access token"
      echo "  --skip     Skip onboarding wizard"
      exit 0 ;;
    *) die "Unknown option: $1" ;;
  esac
done

echo ""
echo -e "${BOLD}═══════════════════════════════════════════${NC}"
echo -e "${BOLD}  🦀 git-agent installer v${VERSION}${NC}"
echo -e "${BOLD}  The repo IS the agent. Git IS the nervous system.${NC}"
echo -e "${BOLD}═══════════════════════════════════════════${NC}"
echo ""

# ---- 1. Check dependencies ----
info "Checking dependencies..."

command -v python3 >/dev/null 2>&1 || die "Python 3.8+ required. Install: https://python.org"
command -v git >/dev/null 2>&1 || die "Git required. Install: https://git-scm.com"
command -v pip3 >/dev/null 2>&1 || command -v pip >/dev/null 2>&1 || warn "pip not found — will install without it"

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
ok "Python ${PYTHON_VERSION}, Git $(git --version | cut -d' ' -f2)"

# ---- 2. Create install directory ----
info "Installing to ${INSTALL_DIR}..."
mkdir -p "${INSTALL_DIR}"/{bin,config,templates,data,logs,vessels}

# ---- 3. Clone or update git-agent ----
if [[ -d "${INSTALL_DIR}/git-agent" ]]; then
  info "Updating existing git-agent..."
  cd "${INSTALL_DIR}/git-agent" && git pull -q 2>/dev/null || warn "Could not update — continuing with existing"
else
  info "Cloning git-agent..."
  git clone -q "${REPO_URL}" "${INSTALL_DIR}/git-agent" 2>/dev/null || warn "Clone failed — install from existing repo"
fi
ok "git-agent source ready"

# ---- 4. Install Python package ----
if [[ -f "${INSTALL_DIR}/git-agent/pyproject.toml" ]]; then
  info "Installing git-agent Python package..."
  cd "${INSTALL_DIR}/git-agent"
  pip3 install -q -e . 2>/dev/null || pip install -q -e . 2>/dev/null || warn "pip install failed — using direct python path"
  ok "Python package installed"
fi

# ---- 5. Create CLI wrapper ----
cat > "${BIN_DIR}/git-agent" << 'WRAPPER'
#!/usr/bin/env bash
# git-agent CLI wrapper
GIT_AGENT_HOME="${GIT_AGENT_HOME:-$HOME/.git-agent}"

if [[ -f "${GIT_AGENT_HOME}/git-agent/src/git_agent/__main__.py" ]]; then
  export PYTHONPATH="${GIT_AGENT_HOME}/git-agent/src:${PYTHONPATH}"
  python3 -m git_agent "$@"
elif command -v git-agent-python >/dev/null 2>&1; then
  git-agent-python "$@"
else
  echo "git-agent not properly installed. Run: bash ${GIT_AGENT_HOME}/git-agent/install.sh"
  exit 1
fi
WRAPPER
chmod +x "${BIN_DIR}/git-agent"
ok "CLI installed at ${BIN_DIR}/git-agent"

# ---- 6. Create onboard script ----
cat > "${BIN_DIR}/git-agent-onboard" << ONBOARD_WRAPPER
#!/usr/bin/env bash
GIT_AGENT_HOME="\${GIT_AGENT_HOME:-\$HOME/.git-agent}"
export PYTHONPATH="\${GIT_AGENT_HOME}/git-agent/src:\${PYTHONPATH}"
python3 "\${GIT_AGENT_HOME}/git-agent/src/git_agent/onboard.py" "\$@"
ONBOARD_WRAPPER
chmod +x "${BIN_DIR}/git-agent-onboard"
ok "Onboard script installed"

# ---- 7. Fleet services config ----
cat > "${INSTALL_DIR}/config/fleet.yaml" << FLEET_CONFIG
# Fleet services — auto-configured
plato:
  url: "http://localhost:8847"
  rooms_auto: true

matrix:
  url: "http://localhost:6167"
  server_name: "147.224.38.131"

arena:
  url: "http://localhost:4044"

keeper:
  url: "http://localhost:8900"

agent_api:
  url: "http://localhost:8901"

crab_trap:
  url: "http://localhost:4042"
FLEET_CONFIG
ok "Fleet services configured"

# ---- 8. Environment setup ----
if ! grep -q "GIT_AGENT_HOME" "$HOME/.bashrc" 2>/dev/null; then
  echo "" >> "$HOME/.bashrc"
  echo "# git-agent" >> "$HOME/.bashrc"
  echo "export GIT_AGENT_HOME=\"${INSTALL_DIR}\"" >> "$HOME/.bashrc"
  echo "export PATH=\"${BIN_DIR}:\$PATH\"" >> "$HOME/.bashrc"
  ok "Added to ~/.bashrc"
fi

export GIT_AGENT_HOME="${INSTALL_DIR}"
export PATH="${BIN_DIR}:${PATH}"

# ---- 9. Onboarding ----
if [[ "$SKIP_ONBOARD" == false ]]; then
  echo ""
  echo -e "${BOLD}═══ Onboarding ═══${NC}"
  echo ""
  
  # GitHub token
  if [[ -z "$TOKEN" ]]; then
    if [[ -n "${GITHUB_TOKEN:-}" ]]; then
      TOKEN="$GITHUB_TOKEN"
      ok "Using GITHUB_TOKEN from environment"
    else
      echo -e "${YELLOW}GitHub token needed for vessel operations.${NC}"
      echo -n "Enter GitHub PAT (or set GITHUB_TOKEN): "
      read -r TOKEN
    fi
  fi

  # Vessel repo
  if [[ -z "$VESSEL" ]]; then
    echo ""
    echo -e "${YELLOW}What vessel does this agent board?${NC}"
    echo "  The vessel repo IS the agent's identity, memory, and career."
    echo "  Examples: SuperInstance/oracle1-workspace, Lucineer/JetsonClaw1-vessel"
    echo ""
    echo -n "Vessel repo (owner/name): "
    read -r VESSEL
  fi

  if [[ -n "$VESSEL" && -n "$TOKEN" ]]; then
    info "Boarding vessel ${VESSEL}..."
    
    # Clone vessel
    VESSEL_DIR="${INSTALL_DIR}/vessels/$(basename "$VESSEL")"
    if [[ -d "$VESSEL_DIR" ]]; then
      cd "$VESSEL_DIR" && git pull -q 2>/dev/null || true
    else
      git clone -q "https://${TOKEN}@github.com/${VESSEL}.git" "$VESSEL_DIR" 2>/dev/null || \
        git clone -q "https://github.com/${VESSEL}.git" "$VESSEL_DIR" 2>/dev/null || \
        warn "Could not clone vessel — will work offline"
    fi
    
    # Write agent config
    AGENT_NAME=$(basename "$VESSEL" | sed 's/-workspace//' | sed 's/-vessel//')
    cat > "${INSTALL_DIR}/config/agent.yaml" << AGENT_CONFIG
# git-agent configuration — auto-generated by onboard
agent:
  name: "${AGENT_NAME}"
  vessel: "${VESSEL}"
  vessel_path: "${VESSEL_DIR}"

github:
  token: "${TOKEN}"

llm:
  provider: "deepinfra"
  model: "ByteDance/Seed-2.0-mini"
  api_key: "\${DEEPINFRA_API_KEY}"
  temperature: 0.7
  max_tokens: 4096

plato:
  url: "http://localhost:8847"
  auto_tile: true

fleet:
  org: "\$(echo $VESSEL | cut -d/ -f1)"
  matrix_server: "http://localhost:6167"

services:
  keeper: "http://localhost:8900"
  agent_api: "http://localhost:8901"
  arena: "http://localhost:4044"
  plato: "http://localhost:8847"
AGENT_CONFIG

    ok "Agent ${AGENT_NAME} boarded vessel ${VESSEL}"
    
    # Read vessel identity files
    if [[ -f "${VESSEL_DIR}/IDENTITY.md" ]]; then
      echo ""
      info "Vessel identity:"
      head -5 "${VESSEL_DIR}/IDENTITY.md" | sed 's/^/  /'
    fi
    if [[ -f "${VESSEL_DIR}/SOUL.md" ]]; then
      echo ""
      info "Soul loaded from SOUL.md"
    fi
    if [[ -f "${VESSEL_DIR}/AGENTS.md" ]]; then
      echo ""
      info "Standing orders loaded from AGENTS.md"
    fi
  fi
fi

# ---- Done ----
echo ""
echo -e "${BOLD}═══════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ git-agent installed and configured${NC}"
echo ""
echo "  CLI:     ${BIN_DIR}/git-agent"
echo "  Config:  ${INSTALL_DIR}/config/agent.yaml"
echo "  Vessel:  ${VESSEL:-not set}"
echo ""
echo "  Start:   git-agent start"
echo "  Chat:    git-agent chat"
echo "  Status:  git-agent status"
echo ""
echo -e "${BOLD}═══════════════════════════════════════════${NC}"
