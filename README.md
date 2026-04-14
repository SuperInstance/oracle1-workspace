# oracle1-workspace

**One‑line description:**  
Python workspace for the Cocapn Fleet (SuperInstance org) that provides core utilities for agent management, knowledge handling, and fleet status monitoring.

---

## What it does
- Supplies the foundational code and documentation for the **Cocapn Fleet** agents.  
- Organizes knowledge bases, memory structures, and identity/soul definitions.  
- Includes tooling, heartbeat monitoring, and status reporting utilities.  
- Serves as a reference implementation for long‑term work and server‑side TODOs.

---

## Installation
```bash
# 1. Clone the repository
git clone https://github.com/SuperInstance/oracle1-workspace.git

# 2. Enter the project directory
cd oracle1-workspace

# 3. (Optional) Set up a virtual environment
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate

# 4. Install any required packages (if a requirements.txt is added later)
# pip install -r requirements.txt
```

---

## Usage
- **Documentation:** See the markdown files in the repo for detailed guidance:
  - `AGENTS.md` – agent definitions and interfaces  
  - `KNOWLEDGE/` – structured knowledge resources  
  - `MEMORY.md`, `IDENTITY.md`, `SOUL.md` – state and identity handling  
  - `TOOLS.md` – helper scripts and utilities  
  - `HEARTBEAT.md`, `STATUS.md` – monitoring and health checks  
  - `FLEET-SERVER-TODO.md`, `LONG-TERM-WORK.md` – roadmap items  

- **Running a component:**  
  ```bash
  python -m oracle1_workspace.agent_manager   # example entry point
  ```

- **Extending:** Add new Python modules under the package directory, update the relevant markdown docs, and commit to the repository.

---

## License
Distributed under the terms of the `LICENSE` file included in the repository.